from numba import njit
import numpy as np

from .utils import (
    _choice,
    _logsumexp,
    _check_array_sums_to_1,
    _check_random_state,
    _argmax,
    check_sequences,
)


__all__ = ["HMM"]


class HMM:
    """Discrete Hidden Markov Model.

    The number of hidden and observable states are determined by the shapes
    of the probability matrices passed as parameters.

    Parameters
    ----------
    init_probas : array-like of shape (n_hidden_states,)
        The initial probabilities.
    transitions : array-like of shape (n_hidden_states, n_hidden_states)
        The transition probabilities. ``transitions[i, j] = P(st+1 = j / st = i)``.
    emissions : array-like of shape (n_hidden_states, n_observable_states)
        The probabilities of symbol emission. ``emissions[i, o] = P(Ot = o /
        st = i)``.
    n_iter : int, default=10
        Number of iterations to run for the EM algorithm (in ``fit()``).

    """

    def __init__(self, init_probas, transitions, emissions, n_iter=10):

        self.init_probas = np.array(init_probas, dtype=np.float64)
        self.transitions = np.array(transitions, dtype=np.float64)
        self.emissions = np.array(emissions, dtype=np.float64)

        self.n_iter = n_iter

        self.n_hidden_states = self.A.shape[0]
        self.n_observable_states = self.B.shape[1]

        if not (
            self.A.shape[0] == self.A.shape[1] == self.pi.shape[0] == self.B.shape[0]
        ):
            raise ValueError("inconsistent number of hidden states.")

        self._check_matrices_conditioning()

    def log_likelihood(self, sequences):
        """Compute log-likelihood of sequences.

        Parameters
        ----------
        sequences : array-like of shape (n_seq, n_obs) or list (or numba typed list) \
                of iterables of variable length
            The sequences of observable states

        Returns
        -------
        log_likelihood : array of shape (n_seq,)
        """
        total_log_likelihood = 0
        sequences, n_obs_max = check_sequences(sequences, return_longest_length=True)
        log_alpha = np.empty(shape=(self.n_hidden_states, n_obs_max), dtype=np.float32)
        for seq in sequences:
            total_log_likelihood += self._forward(seq, log_alpha)
        return total_log_likelihood

    def decode(self, sequences, return_log_probas=False):
        """Decode sequences with Viterbi algorithm.

        Given a sequence of observable states, return the sequence of hidden
        states that most-likely generated the input.

        Parameters
        ----------
        sequences : array-like of shape (n_seq, n_obs) or list (or numba typed list) \
                of iterables of variable length
            The sequences of observable states
        return_log_probas : bool, default=False
            If True, log-probabilities of the joint sequences of observable and
            hidden states are returned

        Returns
        -------
        best_paths : ndarray of shape (n_seq, n_obs) or list of ndarray of \
            variable length
            The most likely sequences of hidden states.
        log_probabilities : ndarray of shape (n_seq,)
            log-probabilities of the joint sequences of observable and hidden
            states. Only present if ``return_log_probas`` is True.
        """
        sequences, n_obs_max = check_sequences(sequences, return_longest_length=True)

        hidden_states_sequences = []
        log_probas = []

        log_V = np.empty(shape=(self.n_hidden_states, n_obs_max), dtype=np.float32)
        back_path = np.empty(shape=(self.n_hidden_states, n_obs_max), dtype=np.int32)

        for seq in sequences:
            n_obs = seq.shape[0]
            self._viterbi(seq, log_V, back_path)
            best_path = np.empty(n_obs, dtype=np.int32)
            log_proba = _get_best_path(log_V, back_path, best_path)
            hidden_states_sequences.append(best_path)
            if return_log_probas:
                log_probas.append(log_proba)

        if isinstance(sequences, np.ndarray):
            # All sequences have the same length
            hidden_states_sequences = np.array(hidden_states_sequences)

        if return_log_probas:
            return hidden_states_sequences, np.array(log_probas)
        else:
            return hidden_states_sequences

    def sample(self, n_seq=10, n_obs=10, random_state=None):
        """Sample sequences of hidden and observable states.

        Parameters
        ----------
        n_seq : int, default=10
            Number of sequences to sample
        n_obs : int, default=10
            Number of observations per sequence
        random_state: int or np.random.RandomState instance, default=None
            Controls the RNG, see `scikt-learn glossary
            <https://scikit-learn.org/stable/glossary.html#term-random-state>`_
            for details.

        Returns
        -------
        hidden_states_sequences : ndarray of shape (n_seq, n_obs)
        observable_states_sequences : ndarray of shape (n_seq, n_obs)
        """
        # TODO: allow n_obs_max

        rng = _check_random_state(random_state)
        sequences = np.array(
            [
                _sample_one(n_obs, self.pi, self.A, self.B, seed=rng.tomaxint())
                for _ in range(n_seq)
            ]
        )
        # Unzip array of (hidden_states, observation) into tuple of arrays
        sequences = sequences.swapaxes(0, 1)
        return sequences[0], sequences[1]

    def fit(self, sequences):
        """Fit model to sequences.

        The probabilities matrices ``init_probas``, ``transitions`` and
        ``emissions`` are estimated with the EM algorithm.

        Parameters
        ----------
        sequences : array-like of shape (n_seq, n_obs) or list (or numba typed list) \
                of iterables of variable length
            The sequences of observable states

        Returns
        -------
        self : HMM instance
        """
        sequences, n_obs_max = check_sequences(sequences, return_longest_length=True)
        log_alpha = np.empty(shape=(self.n_hidden_states, n_obs_max))
        log_beta = np.empty(shape=(self.n_hidden_states, n_obs_max))
        # E[i, j, t] = P(st = i, st+1 = j / O, lambda)
        log_E = np.empty(
            shape=(self.n_hidden_states, self.n_hidden_states, n_obs_max - 1)
        )
        # g[i, t] = P(st = i / O, lambda)
        log_gamma = np.empty(shape=(self.n_hidden_states, n_obs_max))

        for _ in range(self.n_iter):

            self.pi, self.A, self.B = _do_EM_step(
                sequences,
                self._log_pi,
                self._log_A,
                self._log_B,
                log_alpha,
                log_beta,
                log_E,
                log_gamma,
            )
            self._check_matrices_conditioning()
        return self

    def _viterbi(self, seq, log_V, back_path):
        # dummy wrapper for conveniency
        _viterbi(seq, self._log_pi, self._log_A, self._log_B, log_V, back_path)

    def _forward(self, seq, log_alpha):
        # dummy wrapper for conveniency
        return _forward(seq, self._log_pi, self._log_A, self._log_B, log_alpha)

    def _backward(self, seq, log_beta):
        # dummy wrapper for conveniency
        return _backward(seq, self._log_pi, self._log_A, self._log_B, log_beta)

    def _check_matrices_conditioning(self):

        _check_array_sums_to_1(self.pi, "init_probas")
        for s in range(self.n_hidden_states):
            _check_array_sums_to_1(self.A[s], f"Row {s} of A")
            _check_array_sums_to_1(self.B[s], f"Row {s} of B")

    # pi, A and B are respectively init_probas, transitions and emissions
    # matrices. _log_pi, _log_A and _log_B are updated each time pi, A, or B
    # are updated, respectively. Consider these private (and bug-prone :)),
    # Updating transitions would not update _log_A.
    @property
    def pi(self):
        return self.init_probas

    @pi.setter
    def pi(self, value):
        self.init_probas = value
        self._recompute_log_pi = True

    @property
    def _log_pi(self):
        if getattr(self, "_recompute_log_pi", True):
            self.__log_pi = np.log(self.pi)
            self._recompute_log_pi = False
        return self.__log_pi

    @property
    def A(self):
        return self.transitions

    @A.setter
    def A(self, value):
        self.transitions = value
        self._recompute_log_A = True

    @property
    def _log_A(self):
        if getattr(self, "_recompute_log_A", True):
            self.__log_A = np.log(self.A)
            self._recompute_log_A = False
        return self.__log_A

    @property
    def B(self):
        return self.emissions

    @B.setter
    def B(self, value):
        self.emissions = value
        self._recompute_log_B = True

    @property
    def _log_B(self):
        if getattr(self, "_recompute_log_B", True):
            self.__log_B = np.log(self.B)
            self._recompute_log_B = False
        return self.__log_B


@njit(cache=True)
def _sample_one(n_obs, pi, A, B, seed):
    """Return (observations, hidden_states) sample"""
    np.random.seed(seed)  # local to this numba function, not global numpy

    observations = []
    hidden_states = []
    s = _choice(pi)
    for _ in range(n_obs):
        hidden_states.append(s)
        obs = _choice(B[s])
        observations.append(obs)
        s = _choice(A[s])

    return hidden_states, observations


@njit(cache=True)
def _forward(seq, log_pi, log_A, log_B, log_alpha):
    """Fill log_alpha array with log probabilities, return log-likelihood"""
    # alpha[i, t] = P(O1, ... Ot, st = i / lambda)
    # reccursion is alpha[i, t] = B[i, Ot] * sumj(alpha[j, t - 1] * A[i, j])
    # which becomes (when applying log)
    # log_alpha[i, t] = log(B[i, Ot]) +
    #                   logsum_jexp(log_alpha[j, t - 1] + _log_A[i, j])
    # since log(sum(ai . bj)) =
    #       log(sum(exp(log_ai + log_bi)))

    n_obs = len(seq)
    n_hidden_states = log_pi.shape[0]
    log_alpha[:, 0] = log_pi + log_B[:, seq[0]]
    buffer = np.empty(shape=n_hidden_states)
    for t in range(1, n_obs):
        for s in range(n_hidden_states):
            for ss in range(n_hidden_states):
                buffer[ss] = log_alpha[ss, t - 1] + log_A[ss, s]
            log_alpha[s, t] = _logsumexp(buffer) + log_B[s, seq[t]]
    return _logsumexp(log_alpha[:, n_obs - 1])


@njit(cache=True)
def _backward(seq, log_pi, log_A, log_B, log_beta):
    """Fills beta array with log probabilities"""
    # beta[i, t] = P(Ot+1, ... OT, / st = i, lambda)

    n_obs = seq.shape[0]
    n_hidden_states = log_pi.shape[0]
    log_beta[:, n_obs - 1] = np.log(1)
    buffer = np.empty(shape=n_hidden_states)
    for t in range(n_obs - 2, -1, -1):
        for s in range(n_hidden_states):
            for ss in range(n_hidden_states):
                buffer[ss] = log_A[s, ss] + log_B[ss, seq[t + 1]] + log_beta[ss, t + 1]
            log_beta[s, t] = _logsumexp(buffer)


@njit(cache=True)
def _viterbi(seq, log_pi, log_A, log_B, log_V, back_path):
    """Fill V array with log probabilities and back_path with back links"""
    # V[i, t] = max_{s1...st-1} P(O1, ... Ot, s1, ... st-1, st=i / lambda)
    n_obs = seq.shape[0]
    n_hidden_states = log_pi.shape[0]
    log_V[:, 0] = log_pi + log_B[:, seq[0]]
    buffer = np.empty(shape=n_hidden_states)
    for t in range(1, n_obs):
        for s in range(n_hidden_states):
            for ss in range(n_hidden_states):
                buffer[ss] = log_V[ss, t - 1] + log_A[ss, s]
            best_prev = _argmax(buffer)
            back_path[s, t] = best_prev
            log_V[s, t] = buffer[best_prev] + log_B[s, seq[t]]


@njit(cache=True)
def _get_best_path(log_V, back_path, best_path):
    """Fill out best_path array"""
    n_obs = best_path.shape[0]
    s = _argmax(log_V[:, n_obs - 1])
    out = log_V[s, n_obs - 1]
    for t in range(n_obs - 1, -1, -1):
        best_path[t] = s
        s = back_path[s, t]
    return out


@njit(cache=True)
def _do_EM_step(sequences, log_pi, log_A, log_B, log_alpha, log_beta, log_E, log_gamma):
    """Return A, B and C after EM step."""
    # E STEP (over all sequences)
    # Accumulators for parameters of the hmm. They are summed over for
    # each sequence, then normalized in the M-step.
    # These are homogeneous to probabilities, not log-probabilities.
    pi_acc = np.zeros_like(log_pi)
    A_acc = np.zeros_like(log_A)
    B_acc = np.zeros_like(log_B)

    n_hidden_states = log_pi.shape[0]

    for seq_idx in range(len(sequences)):  # numba can't iterate over 2D arrays
        seq = sequences[seq_idx]
        n_obs = seq.shape[0]
        log_likelihood = _forward(seq, log_pi, log_A, log_B, log_alpha)
        _backward(seq, log_pi, log_A, log_B, log_beta)

        # Compute E
        for t in range(n_obs - 1):
            for i in range(n_hidden_states):
                for j in range(n_hidden_states):
                    log_E[i, j, t] = (
                        log_alpha[i, t]
                        + log_A[i, j]
                        + log_B[j, seq[t + 1]]
                        + log_beta[j, t + 1]
                        - log_likelihood
                    )

        # compute gamma
        log_gamma = log_alpha + log_beta - log_likelihood

        # M STEP accumulators
        pi_acc += np.exp(log_gamma[:, 0])
        A_acc += np.sum(np.exp(log_E[:, :, : n_obs - 1]), axis=-1)
        for t in range(n_obs):
            B_acc[:, seq[t]] += np.exp(log_gamma[:, t])

    # M STEP (mostly done in the accumulators already)
    pi = pi_acc / pi_acc.sum()
    # equivalent to X / X.sum(axis=1, keepdims=True) but not supported
    A = A_acc / A_acc.sum(axis=1).reshape(-1, 1)
    B = B_acc / B_acc.sum(axis=1).reshape(-1, 1)

    return pi, A, B

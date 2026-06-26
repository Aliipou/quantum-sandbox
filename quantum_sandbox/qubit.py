"""A single simulated qubit for BB84.

It holds a definite value only in the basis it was prepared/measured in. Measuring
in the *other* basis yields a random outcome and collapses the qubit to that
outcome — this is the simulated 'measurement disturbance' that makes eavesdropping
detectable. There is no `copy()`: you cannot clone an unknown state, only measure
it (and measuring disturbs it).
"""

from __future__ import annotations

import random

RECTILINEAR = 0  # Z basis: |0>, |1>
DIAGONAL = 1     # X basis: |+>, |->


class Qubit:
    def __init__(self, bit: int, basis: int, rng: random.Random | None = None) -> None:
        self._bit = bit
        self._basis = basis
        self._rng = rng or random

    def measure(self, basis: int) -> int:
        if basis == self._basis:
            return self._bit
        # Wrong basis: outcome is random, and the qubit collapses to it.
        outcome = self._rng.randint(0, 1)
        self._bit = outcome
        self._basis = basis
        return outcome

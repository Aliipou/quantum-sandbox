"""BB84 quantum key distribution (simulated).

Alice sends qubits in random bases; Bob measures in random bases; they keep the
positions where bases agreed (sifting) and estimate the error rate (QBER) on a
sample. With no eavesdropper the sifted keys match (QBER 0). An intercept-resend
eavesdropper (Eve) disturbs the qubits and drives QBER toward ~25% — so her
presence is detectable from the error rate alone.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .qubit import Qubit


@dataclass
class BB84Result:
    alice_bases: list[int]
    bob_bases: list[int]
    sifted_alice: list[int]
    sifted_bob: list[int]
    qber: float
    eavesdropper: bool

    @property
    def keys_match(self) -> bool:
        return self.sifted_alice == self.sifted_bob


def run_bb84(
    n: int = 512,
    eavesdropper: bool = False,
    eavesdrop_fraction: float = 1.0,
    seed: int | None = None,
) -> BB84Result:
    """Simulate one BB84 run.

    eavesdrop_fraction lets Eve tap only a fraction of qubits — a smarter attacker
    who trades information for stealth, since QBER scales ~0.25 * fraction.
    """
    rng = random.Random(seed)
    alice_bits = [rng.randint(0, 1) for _ in range(n)]
    alice_bases = [rng.randint(0, 1) for _ in range(n)]
    bob_bases = [rng.randint(0, 1) for _ in range(n)]

    bob_bits: list[int] = []
    for i in range(n):
        q = Qubit(alice_bits[i], alice_bases[i], rng)
        if eavesdropper and rng.random() < eavesdrop_fraction:
            q.measure(rng.randint(0, 1))  # Eve intercepts, measures (disturbs), resends
        bob_bits.append(q.measure(bob_bases[i]))

    sifted_alice, sifted_bob = [], []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_bits[i])

    if sifted_alice:
        errors = sum(1 for a, b in zip(sifted_alice, sifted_bob) if a != b)
        qber = errors / len(sifted_alice)
    else:
        qber = 0.0

    return BB84Result(alice_bases, bob_bases, sifted_alice, sifted_bob, qber, eavesdropper)

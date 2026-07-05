"""Aggressive red-team of the BB84 simulation.

Attacker goal: read the key without being caught by the QBER check. Some attacks
are provably caught (full intercept-resend); one is a real, documented limitation
(low-rate tapping evades a fixed QBER threshold). Statistical claims are pinned so
the model can't silently drift.
"""

import statistics
import unittest

from quantum_sandbox import DIAGONAL, RECTILINEAR, Qubit, run_bb84

ABORT = 0.11  # standard BB84 abort threshold


class TestStatisticalRigor(unittest.TestCase):
    def test_no_eavesdropper_is_always_clean(self):
        for seed in range(30):
            r = run_bb84(n=800, eavesdropper=False, seed=seed)
            self.assertEqual(r.qber, 0.0)
            self.assertTrue(r.keys_match)

    def test_full_eavesdropper_is_always_detected(self):
        for seed in range(30):
            r = run_bb84(n=2000, eavesdropper=True, seed=seed)
            self.assertGreater(r.qber, ABORT, f"Eve slipped under threshold at seed {seed}")

    def test_full_eavesdropper_mean_qber_near_quarter(self):
        qbers = [run_bb84(n=4000, eavesdropper=True, seed=s).qber for s in range(20)]
        self.assertAlmostEqual(statistics.mean(qbers), 0.25, delta=0.02)

    def test_sifting_keeps_about_half(self):
        rate = statistics.mean(
            len(run_bb84(n=4000, seed=s).sifted_alice) / 4000 for s in range(20)
        )
        self.assertAlmostEqual(rate, 0.5, delta=0.03)


class TestAttacks(unittest.TestCase):
    def test_no_cloning_there_is_no_copy_path(self):
        q = Qubit(1, RECTILINEAR)
        self.assertFalse(hasattr(q, "copy"))
        self.assertFalse(hasattr(q, "__copy__"))

    def test_wrong_basis_measurement_disturbs_state(self):
        # Measuring in the wrong basis must be able to flip a later same-basis read.
        flips = 0
        for s in range(200):
            import random
            rng = random.Random(s)
            q = Qubit(0, RECTILINEAR, rng)
            q.measure(DIAGONAL)            # disturb
            if q.measure(RECTILINEAR) != 0:  # original value no longer guaranteed
                flips += 1
        self.assertGreater(flips, 50, "wrong-basis measurement did not disturb the qubit")

    def test_LIMITATION_low_rate_tap_evades_qber_threshold(self):
        # A smarter Eve taps only 20% of qubits: QBER ~5% stays under the 11% abort,
        # so she is NOT caught by the threshold alone. Real BB84 needs privacy
        # amplification + bounded leakage; out of scope for this sandbox. Pinned.
        evaded = 0
        for s in range(20):
            r = run_bb84(n=3000, eavesdropper=True, eavesdrop_fraction=0.2, seed=s)
            if r.qber < ABORT:
                evaded += 1
        self.assertGreater(evaded, 15, "LIMITATION changed: low-rate tap now caught?")


class TestEdgeCases(unittest.TestCase):
    def test_zero_length(self):
        r = run_bb84(n=0, eavesdropper=True, seed=1)
        self.assertEqual(r.qber, 0.0)
        self.assertEqual(r.sifted_alice, [])

    def test_single_qubit_does_not_crash(self):
        r = run_bb84(n=1, eavesdropper=True, seed=1)
        self.assertIn(len(r.sifted_alice), (0, 1))


if __name__ == "__main__":
    unittest.main()

import unittest

from quantum_sandbox import DIAGONAL, RECTILINEAR, Qubit, run_bb84


class TestQubit(unittest.TestCase):
    def test_same_basis_is_deterministic(self):
        q = Qubit(1, RECTILINEAR)
        self.assertEqual(q.measure(RECTILINEAR), 1)
        self.assertEqual(q.measure(RECTILINEAR), 1)  # stable once measured in-basis

    def test_no_clone_only_measure(self):
        # The API exposes no copy(); you can only measure (which disturbs).
        self.assertFalse(hasattr(Qubit(0, DIAGONAL), "copy"))


class TestBB84(unittest.TestCase):
    def test_no_eavesdropper_keys_match_qber_zero(self):
        r = run_bb84(n=1000, eavesdropper=False, seed=7)
        self.assertEqual(r.qber, 0.0)
        self.assertTrue(r.keys_match)
        self.assertGreater(len(r.sifted_alice), 300)  # ~half of n survive sifting

    def test_eavesdropper_raises_qber(self):
        r = run_bb84(n=2000, eavesdropper=True, seed=7)
        # intercept-resend drives QBER toward ~25%, well above the 11% abort line
        self.assertGreater(r.qber, 0.15)
        self.assertFalse(r.keys_match)

    def test_deterministic_with_seed(self):
        a = run_bb84(n=500, eavesdropper=True, seed=42)
        b = run_bb84(n=500, eavesdropper=True, seed=42)
        self.assertEqual(a.qber, b.qber)
        self.assertEqual(a.sifted_bob, b.sifted_bob)


if __name__ == "__main__":
    unittest.main()

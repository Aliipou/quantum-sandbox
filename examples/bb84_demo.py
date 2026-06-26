"""Run BB84 with and without an eavesdropper and watch the QBER give Eve away.

    python examples/bb84_demo.py
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantum_sandbox import run_bb84


def main() -> None:
    print("BB84 quantum key distribution (simulated)")
    print("=" * 50)

    clean = run_bb84(n=2000, eavesdropper=False, seed=1)
    print(f"\nNo eavesdropper:")
    print(f"  sifted key length: {len(clean.sifted_alice)}")
    print(f"  QBER: {clean.qber:.3%}   keys match: {clean.keys_match}")

    tapped = run_bb84(n=2000, eavesdropper=True, seed=1)
    print(f"\nWith eavesdropper (intercept-resend):")
    print(f"  sifted key length: {len(tapped.sifted_alice)}")
    print(f"  QBER: {tapped.qber:.3%}   keys match: {tapped.keys_match}")

    threshold = 0.11  # standard BB84 abort threshold
    print(f"\nAbort threshold: {threshold:.0%}")
    print(f"  clean run  -> {'KEEP key' if clean.qber < threshold else 'ABORT'}")
    print(f"  tapped run -> {'KEEP key' if tapped.qber < threshold else 'ABORT (eavesdropper detected)'}")


if __name__ == "__main__":
    main()

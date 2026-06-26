# quantum-sandbox — threat model (honest)

This is a **simulation**, T3 research. It proves a property in code; it provides no
real security. The "attacker" is Eve trying to learn the key without raising QBER.

| Attack | Result |
|--------|--------|
| Full intercept-resend | ✅ always detected — QBER → ~25%, above the 11% abort line (30 seeds) |
| Clone the unknown qubit | ✅ impossible by construction — `Qubit` exposes no `copy()`; only `measure()`, which disturbs |
| **Low-rate tapping (e.g. 20%)** | ❌ **evades the QBER threshold** — QBER ~5% < 11%. Eve trades information for stealth. Pinned as `test_LIMITATION_low_rate_tap_evades_qber_threshold`. |

## Known limitations (do not claim beyond these)

- **No privacy amplification / error correction.** Real BB84 bounds Eve's residual
  information after a low-rate tap via privacy amplification; this sandbox only
  computes QBER, so a partial tapper leaks information undetected. Out of scope.
- **Ideal channel.** No real channel noise; here QBER=0 means "no Eve" exactly,
  which a real noisy channel never gives. The 11% threshold exists precisely to
  separate noise from eavesdropping — not modelled here.
- **It is a classical simulation.** No real qubits, no real security. For production
  confidentiality/integrity, use **PQC** in AuthGate's crypto provider, not this.

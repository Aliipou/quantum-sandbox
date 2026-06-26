# quantum-sandbox

An **independent quantum research sandbox** — pure-Python simulation of quantum
key distribution (BB84), built to study one property in code: that eavesdropping
on an unknown quantum state is physically **detectable**.

> **Honest status (read this).** This is **research, tier T3**. It is a *classical
> simulation* — there are no real qubits, no real quantum hardware, and **no real
> quantum security**. It depends on nothing and nothing depends on it. It is not a
> production component and must never be treated as one.

## Where it sits

A *completely separate research* project in the ecosystem — by design it has **no
technical dependency** on AuthGate, qfl, banking, or anything else. If quantum
networking never becomes practical, this repo can be deleted and nothing else
changes. For production confidentiality/integrity, the answer is **PQC inside
AuthGate's crypto provider**, not this. Quantum here is a research curiosity, not
the foundation of anything.

## What it shows

BB84: Alice sends qubits in random bases, Bob measures in random bases, they keep
the positions where bases agreed (sifting), and estimate the error rate (QBER).

- **No eavesdropper** → sifted keys match, QBER = 0.
- **Intercept-resend eavesdropper** → measuring in the wrong basis disturbs the
  qubits, driving QBER toward ~25% — above the standard 11% abort threshold, so
  Eve is detected from the error rate alone.

No-cloning is modelled honestly: a `Qubit` exposes no `copy()`; you can only
`measure()` it, and measuring in the wrong basis collapses it.

## Run

```bash
python examples/bb84_demo.py        # see clean vs. tapped QBER
python -m unittest discover -s tests -t .
```

Stdlib only. Zero dependencies.

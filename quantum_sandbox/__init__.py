"""quantum-sandbox — an independent quantum research sandbox (T3, simulation only).

Pure-Python simulation of quantum key distribution (BB84). No real qubits, no real
security, no dependency on any production system. Its purpose is to study, in code,
the one quantum property that actually matters for trust: that eavesdropping on an
unknown quantum state is physically detectable (measurement disturbance).
"""

from .bb84 import BB84Result, run_bb84
from .qubit import DIAGONAL, RECTILINEAR, Qubit

__version__ = "0.1.0"

__all__ = ["Qubit", "RECTILINEAR", "DIAGONAL", "BB84Result", "run_bb84", "__version__"]

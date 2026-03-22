"""
smoothing.py — smoothing utilities for modulation signals.
"""

import numpy as np

def lowpass(signal, alpha=0.1):
    """Simple one‑pole lowpass smoothing."""
    out = np.zeros_like(signal)
    out[0] = signal[0]
    for i in range(1, len(signal)):
        out[i] = alpha * signal[i] + (1 - alpha) * out[i-1]
    return out

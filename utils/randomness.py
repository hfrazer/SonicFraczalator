"""
randomness.py — random helpers for chaos‑driven modulation.
"""

import numpy as np

def jitter(value, amount):
    """Apply small random variation."""
    return value + np.random.uniform(-amount, amount)

def random_walk(prev, step=0.01):
    """Simple bounded random walk."""
    nxt = prev + np.random.uniform(-step, step)
    return np.clip(nxt, -1, 1)

"""
envelope.py — amplitude envelope generators for the SONICFRACZALATOR.
"""

import numpy as np

def adsr(attack, decay, sustain, release, total_samples, sample_rate):
    """
    Generate an ADSR envelope.

    attack, decay, release in seconds
    sustain in [0,1]
    """
    a = int(attack * sample_rate)
    d = int(decay * sample_rate)
    r = int(release * sample_rate)
    s = max(total_samples - (a + d + r), 0)

    attack_curve = np.linspace(0, 1, a, endpoint=False)
    decay_curve = np.linspace(1, sustain, d, endpoint=False)
    sustain_curve = np.full(s, sustain)
    release_curve = np.linspace(sustain, 0, r)

    return np.concatenate([attack_curve, decay_curve, sustain_curve, release_curve])

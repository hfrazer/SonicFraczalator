# mixdown.py
# Final stereo summing stage for SONICFRACZALATOR

import numpy as np

class Mixdown:
    def __init__(self, params):
        self.params = params

    def mix(self, voice_signals):
        """
        voice_signals = list of (left, right) arrays
        Returns (left, right) float32 arrays
        """

        # Assume all voices have same length
        num_samples = len(voice_signals[0][0])

        left  = np.zeros(num_samples, dtype=np.float32)
        right = np.zeros(num_samples, dtype=np.float32)

        # Sum all voices
        for (L, R) in voice_signals:
            left  += L
            right += R

        # Normalise like legacy Fractal‑Chords
        peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
        if peak > 0:
            left  /= peak * 1.01
            right /= peak * 1.01

        return left, right

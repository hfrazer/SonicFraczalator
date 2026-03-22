# phase_shift.py
# Per-voice chaotic lane phase shifting (ported from legacy Fractal-Chords)

import numpy as np
import math

class PhaseShift:
    def __init__(self, mode="even"):
        self.mode = mode.lower()

    def compute_shift(self, voice_index, num_voices, length):
        """Return the integer shift amount for this voice."""
        if self.mode == "even":
            return int((voice_index / num_voices) * length)

        elif self.mode == "random":
            return np.random.randint(0, length)

        elif self.mode == "golden_ratio":
            phi = (math.sqrt(5) - 1) / 2
            return int(((voice_index * phi) % 1) * length)

        else:
            raise ValueError(f"Unknown phase shift mode: {self.mode}")

    def apply(self, X, Y, Z, voice_index, num_voices):
        """Return (Xi, Yi, Zi) for this voice."""
        length = len(X)
        shift = self.compute_shift(voice_index, num_voices, length)

        Xi = np.roll(X, shift)
        Yi = np.roll(Y, shift)
        Zi = np.roll(Z, shift)

        return Xi, Yi, Zi

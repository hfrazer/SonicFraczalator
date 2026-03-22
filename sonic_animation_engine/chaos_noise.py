# chaos_noise.py
# Chaotic noise field for SONICFRACZALATOR
# Ports the legacy Fractal‑Chords chaos noise behaviour

import numpy as np


class ChaosNoise:
    def __init__(self, params):
        self.params = params

    def generate(self, X, Y, Z):
        """
        Build a chaotic noise field from attractor lanes X, Y, Z.
        Matches the legacy behaviour:
          - magnitude of derivatives
          - random jitter
          - smoothing
          - normalisation
        """
        if not self.params.ENABLE_CHAOS_NOISE:
            return np.zeros_like(X)

        # Derivative magnitudes
        dX = np.abs(np.diff(X, prepend=X[0]))
        dY = np.abs(np.diff(Y, prepend=Y[0]))
        dZ = np.abs(np.diff(Z, prepend=Z[0]))

        chaos = (dX + dY + dZ) / 3.0

        # Normalise
        chaos = self._norm(chaos)

        # Random jitter
        chaos += self.params.CHAOS_NOISE_RANDOM * np.random.randn(len(chaos))

        # Smoothing
        kernel_size = int(self.params.CHAOS_NOISE_SMOOTH)
        if kernel_size > 1:
            kernel = np.ones(kernel_size) / kernel_size
            chaos = np.convolve(chaos, kernel, mode="same")

        # Final normalisation
        chaos = self._norm(chaos)
        return chaos

    @staticmethod
    def _norm(v):
        v = v - v.min()
        denom = (v.max() - v.min()) + 1e-9
        return v / denom

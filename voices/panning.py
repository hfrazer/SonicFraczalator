# panning.py
# Stereo panning engine for SONICFRACZALATOR
# Ports the legacy chaotic stereo behaviour

import numpy as np

class PanningEngine:
    def __init__(self, depth=1.0):
        self.depth = depth

    def compute_pan(self, Xi_value, Yi_value):
        """
        Legacy behaviour:
        pan = PAN_DEPTH * sin((Xi + Yi) * pi * 2)
        """
        return self.depth * np.sin((Xi_value + Yi_value) * np.pi * 2)

    def apply(self, sample, Xi_value, Yi_value):
        """
        Return (left, right) stereo sample.
        """
        pan = self.compute_pan(Xi_value, Yi_value)

        left  = sample * (0.5 * (1 - pan))
        right = sample * (0.5 * (1 + pan))

        return left, right

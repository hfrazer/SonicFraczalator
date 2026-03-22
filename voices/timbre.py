# timbre.py
# Timbre morphing engine for SONICFRACZALATOR
# Ports the legacy sine→square morphing behaviour

import numpy as np

class TimbreEngine:
    def __init__(self, depth=1.0):
        self.depth = depth

    def compute_timbre(self, Y_value):
        """
        Legacy behaviour:
        timbre = TIMBRE_DEPTH * abs(sin(Yi[i] * pi))
        """
        return self.depth * abs(np.sin(Y_value * np.pi))

    def apply(self, sine, square, Y_value):
        """
        Return the timbre-morphed sample.
        """
        t = self.compute_timbre(Y_value)
        return (1 - t) * sine + t * square

# oscillators.py
# Core oscillators for SONICFRACZALATOR
# Ports the legacy sine + square + phase accumulator behaviour

import numpy as np

class PhaseAccumulator:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.phase = 0.0

    def advance(self, freq):
        """Advance phase by one sample and return new phase."""
        self.phase += 2 * np.pi * freq / self.sample_rate
        return self.phase


class Oscillators:
    @staticmethod
    def sine(phase):
        return np.sin(phase)

    @staticmethod
    def square(phase):
        s = np.sin(phase)
        return np.sign(s) if s != 0 else 1.0

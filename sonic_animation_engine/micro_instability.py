# micro_instability.py
# Micro-instability module: adds subtle drift, jitter, and breathing motion

import math
import random

class MicroInstability:
    def __init__(self, params):
        self.params = params
        random.seed(self.params.MICRO_INSTABILITY_SEED)

        # Internal drift phase for slow wandering
        self.phase = random.random() * 1000.0

    def apply(self, voice_state, t):
        """
        Applies subtle drift to any numeric values inside voice_state.
        This is intentionally generic — it decorrelates parameters without
        assuming a specific synth architecture.
        """

        depth = self.params.MICRO_INSTABILITY_DEPTH
        rate = self.params.MICRO_INSTABILITY_RATE

        if depth <= 0.0:
            return voice_state

        # Compute a slow drift value
        drift = depth * math.sin(2 * math.pi * rate * t + self.phase)

        # Apply drift to any numeric fields in voice_state
        new_state = {}
        for key, value in voice_state.items():
            if isinstance(value, (int, float)):
                new_state[key] = value + drift
            else:
                new_state[key] = value

        return new_state

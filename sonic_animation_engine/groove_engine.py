# groove_engine.py
# Groove Engine: injects timing swing, micro-variations, and rhythmic life

import math
import random

class GrooveEngine:
    def __init__(self, params):
        self.params = params
        random.seed(99991)  # independent seed for groove randomness

        # Internal LFO phase
        self.phase = random.random() * 1000.0

    def apply(self, voice_state, t):
        """
        Applies groove modulation to timing-related parameters.
        This version assumes voice_state may contain a 'time_offset' field.
        """

        depth = self.params.GROOVE_DEPTH
        swing = self.params.GROOVE_SWING
        variance = self.params.GROOVE_VARIANCE
        rate = self.params.GROOVE_RATE

        if depth <= 0.0:
            return voice_state

        # LFO-based swing
        swing_offset = depth * swing * math.sin(2 * math.pi * rate * t + self.phase)

        # Random micro-variance
        jitter = depth * variance * (random.random() * 2 - 1)

        total_offset = swing_offset + jitter

        new_state = dict(voice_state)

        # Apply to any timing-related field
        if "time_offset" in new_state and isinstance(new_state["time_offset"], (int, float)):
            new_state["time_offset"] += total_offset
        else:
            # If no timing field exists, create one
            new_state["time_offset"] = total_offset

        return new_state

import numpy as np

class BehaviourEngine:
    def __init__(self, params):
        self.on = params.BEHAVIOUR_MOD_ON
        self.depth = params.BEHAVIOUR_MOD_DEPTH
        self.sensitivity = params.BEHAVIOUR_MOD_SENSITIVITY
        self.smoothing = params.BEHAVIOUR_MOD_SMOOTHING

        self.prev = 0.0

    def apply(self, behaviour_state, Yi, Zi):
        if not self.on:
            return behaviour_state

        # Behaviour signal from attractor motion
        behaviour_signal = (abs(Yi) + abs(Zi)) * 0.5

        # Sensitivity scaling
        behaviour_signal *= self.sensitivity

        # Smoothing (simple one-pole lowpass)
        smoothed = (
            self.prev * (1 - self.smoothing)
            + behaviour_signal * self.smoothing
        )
        self.prev = smoothed

        # Apply behaviour modulation
        behaviour_state["brightness"] += smoothed * self.depth
        behaviour_state["amp_shape"] += smoothed * self.depth * 0.5
        behaviour_state["chaos_depth"] += smoothed * self.depth * 0.3

        return behaviour_state

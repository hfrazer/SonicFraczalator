# behaviour_mod.py
# Behavioural modulation: interprets attractor motion musically

class BehaviourMod:
    def __init__(self, params):
        self.params = params

        # Internal smoothing state
        self.prev_mod = 0.0

    def apply(self, voice_state, attractor_state):
        """
        Uses attractor motion to influence musical behaviour.
        This version uses attractor velocity as a generic 'energy' signal.
        """

        depth = self.params.BEHAVIOUR_MOD_DEPTH
        sensitivity = self.params.BEHAVIOUR_MOD_SENSITIVITY
        smoothing = self.params.BEHAVIOUR_MOD_SMOOTHING

        if depth <= 0.0:
            return voice_state

        # Expect attractor_state to contain x, y, z
        x = attractor_state.get("x", 0.0)
        y = attractor_state.get("y", 0.0)
        z = attractor_state.get("z", 0.0)

        # Compute a simple 'energy' measure
        energy = abs(x) + abs(y) + abs(z)

        # Sensitivity scaling
        mod = energy * sensitivity * depth

        # Smooth it
        mod = smoothing * self.prev_mod + (1 - smoothing) * mod
        self.prev_mod = mod

        # Apply modulation to numeric voice parameters
        new_state = {}
        for key, value in voice_state.items():
            if isinstance(value, (int, float)):
                new_state[key] = value * (1.0 + mod)
            else:
                new_state[key] = value

        return new_state

"""
thomas.py — Thomas attractor for the SONICFRACZALATOR.
"""

import numpy as np

class ThomasAttractor:
    def __init__(self, x=0.1, y=0.0, z=0.0, dt=0.01, b=0.208186):
        self.x = x
        self.y = y
        self.z = z
        self.dt = dt
        self.b = b  # Standard Thomas parameter

    def step(self):
        x, y, z = self.x, self.y, self.z

        dx = np.sin(y) - self.b * x
        dy = np.sin(z) - self.b * y
        dz = np.sin(x) - self.b * z

        self.x += dx * self.dt
        self.y += dy * self.dt
        self.z += dz * self.dt

        return np.array([self.x, self.y, self.z], dtype=np.float32)

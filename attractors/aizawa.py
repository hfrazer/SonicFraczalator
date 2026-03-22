"""
aizawa.py — Aizawa attractor for the SONICFRACZALATOR.
"""

import numpy as np

class AizawaAttractor:
    def __init__(self, x=0.1, y=0.0, z=0.0, dt=0.01):
        self.x = x
        self.y = y
        self.z = z
        self.dt = dt

        # Standard Aizawa parameters
        self.a = 0.95
        self.b = 0.7
        self.c = 0.6
        self.d = 3.5
        self.e = 0.25
        self.f = 0.1

    def step(self):
        x, y, z = self.x, self.y, self.z

        dx = (z - self.b) * x - self.d * y
        dy = self.d * x + (z - self.b) * y
        dz = self.c + self.a * z - (z**3) / 3 - (x**2 + y**2) * (1 + self.e * z) + self.f * z * x**3

        self.x += dx * self.dt
        self.y += dy * self.dt
        self.z += dz * self.dt

        return np.array([self.x, self.y, self.z], dtype=np.float32)

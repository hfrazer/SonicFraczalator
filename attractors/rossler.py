# rossler.py
# Simple Rössler attractor integrator for modulation

class RosslerAttractor:
    def __init__(self, x=0.1, y=0.0, z=0.0, a=0.2, b=0.2, c=5.7, dt=0.01):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
        self.dt = dt

    def step(self):
        dx = -self.y - self.z
        dy = self.x + self.a * self.y
        dz = self.b + self.z * (self.x - self.c)

        self.x += dx * self.dt
        self.y += dy * self.dt
        self.z += dz * self.dt

        return {"x": self.x, "y": self.y, "z": self.z}

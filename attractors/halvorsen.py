class HalvorsenAttractor:
    def __init__(self, x=0.1, y=0.0, z=0.0, a=1.4, dt=0.01):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.dt = dt

    def step(self):
        dx = -self.a * self.x - 4*self.y - 4*self.z - self.y*self.y
        dy = -self.a * self.y - 4*self.z - 4*self.x - self.z*self.z
        dz = -self.a * self.z - 4*self.x - 4*self.y - self.x*self.x

        self.x += dx * self.dt
        self.y += dy * self.dt
        self.z += dz * self.dt

        return {"x": self.x, "y": self.y, "z": self.z}

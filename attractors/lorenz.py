class LorenzAttractor:
    def __init__(self, x=0.1, y=0.0, z=0.0, sigma=10.0, rho=28.0, beta=8/3, dt=0.01):
        self.x = x
        self.y = y
        self.z = z
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.dt = dt

    def step(self):
        dx = self.sigma * (self.y - self.x)
        dy = self.x * (self.rho - self.z) - self.y
        dz = self.x * self.y - self.beta * self.z

        self.x += dx * self.dt
        self.y += dy * self.dt
        self.z += dz * self.dt

        return {"x": self.x, "y": self.y, "z": self.z}

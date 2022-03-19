import numpy as np


class DiffusiveSIR(object):
    N = 0
    initial = None
    particles = None
    D = 100
    t0 = 0.1
    dt = 0.01
    L = 10.0

    def __init__(self, N: int):
        self.N = N
        self.particles = np.zeros((N, 2))

        self.initial_position()

    def initial_position(self):
        self.particles = self.L * np.random.rand(self.N, 2)

    def evolve(self, t_max: int):
        const = np.sqrt(2.0 * self.D * self.dt)

        for t in range(t_max):
            for i in range(self.N):
                self.particles[i, 0] += const * np.random.normal() + self.L
                self.particles[i, 1] += const * np.random.normal() + self.L
                self.particles[i, :] %= self.L

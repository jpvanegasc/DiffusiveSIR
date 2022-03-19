import numpy as np


class DiffusiveSIR(object):
    N = 0
    initial = None
    particles = None
    D = 100
    t0 = 0.1
    dt = 0.01
    L = 10.0
    sigma = []

    def __init__(self, N: int):
        self.N = N
        self.particles = np.zeros((N, 2))

        self.initial_position()

    def initial_position(self):
        # self.particles = self.L * np.random.rand(self.N, 2)
        self.particles = np.array(
            [
                [
                    0.5 * self.L + 0.5 * np.random.random(),
                    0.5 * self.L + 0.5 * np.random.random(),
                ]
                for _ in range(self.N)
            ]
        )

    def evolve(self, t_max: int):
        const = np.sqrt(2.0 * self.D * self.dt)

        for t in range(t_max):
            # Move with periodic boundaries
            dx = const * np.random.normal(size=(self.N, 2))
            self.particles += dx + self.L
            self.particles %= self.L

            # Calculate standard deviation
            sigma_x, sigma_y = np.std(self.particles, axis=0)
            self.sigma.append([self.dt * t, sigma_x, sigma_y])

        self.sigma = np.array(self.sigma)

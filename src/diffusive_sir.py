import numpy as np


class DiffusiveSIR(object):
    N = 0
    initial = None
    particles = None
    health = None
    health_time = None
    sigma = []
    D = 100
    t0 = 0.1
    dt = 0.01
    L = 10.0
    sick_time = 1.0

    mapping = {
        0: "black",  # healthy
        1: "red",  # infected
        2: "yellow",  # recovered
    }

    def __init__(self, N: int, infected: int):
        self.N = N
        self.particles = np.zeros((N, 2))
        self.health = np.zeros(N, dtype=int)
        self.health_time = np.zeros(N)

        self.initial_position()
        self.infect(infected)

    def initial_position(self):
        self.particles = self.L * np.random.rand(self.N, 2)

    def infect(self, infected: int):
        for _ in range(infected):
            flag = True
            while flag:
                i = np.random.randint(0, self.N)
                if self.health[i] != 1:
                    self.health[i] = 1
                    flag = False

    def get_health_color(self, health: int):
        return self.mapping.get(health, "black")

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

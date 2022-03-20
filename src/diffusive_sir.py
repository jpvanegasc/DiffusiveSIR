import numpy as np


class DiffusiveSIR(object):
    health_time = {}
    sigma = []
    D = 100
    t0 = 0.1
    dt = 0.01
    L = 10.0
    recovery_time = 1.0
    sick_distance = 1.0
    sick_prob = 0.5

    mapping = {
        0: "black",  # healthy
        1: "red",  # infected
        2: "yellow",  # recovered
    }

    def __init__(self, N: int, infected: float):
        self.N = N
        self.particles = np.zeros((N, 2))
        self.health = np.zeros(N, dtype=int)

        self.initial_position()
        self.infect(int(N * infected))

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

    def check_infected(self):
        for i in range(self.N):
            if self.health[i] == 1:  # Already infected
                continue

            for j in range(i + 1, self.N):
                if self.health[j] != 1:  # Only infected can infect
                    continue

                norm = np.linalg.norm(self.particles[i, :] - self.particles[j, :])
                r = np.random.random()

                if norm <= self.sick_distance and r > self.sick_prob:
                    self.health[i] = 1
                    self.health_time[i] = 0.0
                    break

    def add_sick_time(self):
        for i in self.health_time:
            self.health_time[i] += self.dt

    def check_recovered(self):
        for i, v in list(self.health_time.items()):  # force copy of items
            if v >= self.recovery_time:
                self.health[i] = 2
                self.health_time.pop(i)

    def evolve(self, t_max: int):
        const = np.sqrt(2.0 * self.D * self.dt)

        for t in range(t_max):
            # Move with periodic boundaries
            dx = const * np.random.normal(size=(self.N, 2))
            self.particles += dx + self.L
            self.particles %= self.L

            self.check_infected()
            self.add_sick_time()

            self.check_recovered()

            sigma_x, sigma_y = np.std(self.particles, axis=0)
            self.sigma.append([self.dt * t, sigma_x, sigma_y])

        self.sigma = np.array(self.sigma)

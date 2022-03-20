import numpy as np


class DiffusiveSIR(object):
    health_time = {}
    sigma = []
    healthy = []
    infected = []
    recovered = []
    healthy_indices = []
    infected_indices = []
    recovered_indices = []
    D = 100
    t0 = 0.1
    dt = 0.01
    L = 10.0
    recovery_time = 1.0
    infected_distance = 1.0
    infected_prob = 0.5

    mapping = {
        0: "black",  # healthy
        1: "red",  # infected
        2: "yellow",  # recovered
    }

    def __init__(self, N: int, infected: float, density: float):
        self.N = N
        self.L = np.sqrt(N / density)

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

    def get_indices_by_health(self):
        self.healthy_indices.clear()
        self.infected_indices.clear()
        self.recovered_indices.clear()

        for i in range(self.N):
            if self.health[i] == 0:
                self.healthy_indices.append(i)
            elif self.health[i] == 1:
                self.infected_indices.append(i)
            else:
                self.recovered_indices.append(i)

    def check_infected(self):
        self.get_indices_by_health()

        for i in self.healthy_indices:  # Only healthy can get infected
            for j in self.infected_indices:  # Only infected can infect
                norm = np.linalg.norm(self.particles[i, :] - self.particles[j, :])
                r = np.random.random()

                if norm <= self.infected_distance and r > self.infected_prob:
                    self.health[i] = 1
                    self.health_time[i] = 0.0
                    break

    def add_infected_time(self):
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
            self.add_infected_time()

            self.check_recovered()

            # Commented because an 'if' is computationally expensive
            # sigma_x, sigma_y = np.std(self.particles, axis=0)
            # self.sigma.append([self.dt * t, sigma_x, sigma_y])

            self.healthy.append([t, sum(map(lambda x: x == 0, self.health))])
            self.infected.append([t, sum(map(lambda x: x == 1, self.health))])
            self.recovered.append([t, sum(map(lambda x: x == 2, self.health))])

            progress = int(50 * t / t_max)
            missing = int(50 - progress)
            print(f"0% [{'#'*progress}{' '*missing}] 100%", flush=True, end="\r")

        print(f"0% [{'#'*50}] 100%")

        self.sigma = np.array(self.sigma)
        self.healthy = np.array(self.healthy)
        self.infected = np.array(self.infected)
        self.recovered = np.array(self.recovered)

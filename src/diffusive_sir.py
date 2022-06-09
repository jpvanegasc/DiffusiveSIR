import numpy as np
import matplotlib.pyplot as plt

from plot import plot_particles

class DiffusiveSIR(object):
    health_time = {}
    sigma = []
    sir = []
    confined_Time = {}

    D = 100 # m2/day
    dt = 0.01  # day
    recovery_time = 14.0  # day
    infected_distance = 2.0  # m
    infected_prob = 0.2
    confined_time = 5.0 #days

    mapping = {
        0: "darkgreen",  # susceptible
        1: "darkred",  # infected
        2: "orange",  # recovered
        3: "blue",  # confined
    }

    def __init__(self, N: int, infected: float, density: float):
        self.N = N
        self.L = np.sqrt(N / density)

        self.particles = np.zeros((N, 3))  # (x,y,health)

        self.initial_position()
        self.infect(int(N * infected))

    def initial_position(self):
        self.particles[:, :2] = self.L * np.random.rand(self.N, 2)

    def infect(self, infected: int):
        for _ in range(infected):
            flag = True
            while flag:
                i = np.random.randint(0, self.N)
                if self.particles[i, 2] != 1:
                    self.particles[i, 2] = 1
                    flag = False

    def get_health_color(self, health: int):
        return self.mapping.get(health, "black")

    def get_indices_by_health(self):
        susceptible = []
        infected = []
        recovered = []
        sick = []

        for i in range(self.N):
            if self.particles[i, 2] == 0:
                susceptible.append(i)
            elif (self.particles[i, 2] == 1 or self.particles[i, 2] == 3):
                infected.append(i)
                sick.append(i)
            else:
                recovered.append(i)
                sick.append(i)

        return susceptible, infected, recovered , sick

    def check_infected(self, susceptible, infected):
        for i in susceptible:  # Only susceptible can get infected
            for j in infected:  # Only infected can infect
                if self.particles[j, 2] == 1:
                    norm = np.linalg.norm(self.particles[i, :2] - self.particles[j, :2])
                    r = np.random.random()

                    if norm <= self.infected_distance and r <= self.infected_prob:
                        self.particles[i, 2] = 1
                        self.health_time[i] = 0.0
                        break

    def confined(self, infected):
        N_infected = []
        for j in infected :
            if self.particles[j, 2] == 1 :
                N_infected.append(j)
        P_infected = len(N_infected) / self.N
        P_confined = 0.3
        if (P_infected >= 0.2):
            k = int(len(N_infected) * P_confined)
            for _ in range(k):
                i = np.random.randint(0, len(N_infected))
                ii = N_infected[i]
                self.particles[ii, 2] = 3
                self.confined_Time[ii] = 0.0

    def add_infected_time(self):
        for i in self.health_time:
            self.health_time[i] += self.dt

    def check_recovered(self):
        for i, v in list(self.health_time.items()):  # force copy of items
            if v >= self.recovery_time:
                self.particles[i, 2] = 2
                self.health_time.pop(i)

    def add_confined_time(self):
        for i in self.confined_Time:
            self.confined_Time[i] += self.dt

    def check_restraint(self):
        for i, t in list(self.confined_Time.items()):
            if ( t >= self.confined_time 
                and self.particles[i, 2] == 3 ):
                self.particles[i, 2] = 1
                self.confined_Time.pop(i)

    def plot_timestep(self, filename: str , xlabel: str, ylabel: str, title: str, size=10):
        colors = list(
            map(lambda h: self.get_health_color(h), self.particles[:, 2])
        )
        plot_particles(
            self.particles,
            self.L,
            self.L,
            color=colors,
            size=size,
        )
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(filename)
        plt.close()

    def evolve(self, t_max: int):
        sigma = 2.0 * self.D * self.dt
        const = np.sqrt(sigma) / np.sqrt(2)
        f_o = np.sqrt(2) * 0.348

        self.sir = np.zeros((t_max, 4))
        marker_size = 23 * np.exp(-0.0005 * self.N) + 7

        for t in range(t_max):
            # Move with periodic boundaries
            """
            if t%4 == 0 :   #create the gif of infection spread
                t1 = t * self.dt
                t2 = t + 100000
                self.plot_timestep("../data/gif/"+ str(t2) +".png", "m", "m", "Position at "+str(t1)+" days", marker_size)
            """

            dx = f_o * const * np.random.normal(size=(self.N, 2))
            self.particles[:, :2] += dx + self.L
            self.particles[:, :2] %= self.L

            """
            dx = const * np.random.normal(size=(self.N, 2)) #*(1/Daniel)
            #self.particles[:, :2] += dx + self.L
            #self.particles[:, :2] %= self.L
            self.particles[:, :2] = abs( self.particles[:, :2] + dx)

            for ii in range(self.N):
                if(self.particles[ii, 0]): self.particles[ii, 0] -= 2*dx[ii, 0]
                if(self.particles[ii, 1]): self.particles[ii, 1] -= 2*dx[ii, 1]
            """

            s, i, r, ns = self.get_indices_by_health()

            self.check_infected(s, i)
            self.add_infected_time()
            self.check_recovered()

            if (t >= 1000):
                self.confined(i)
                self.add_confined_time()
                self.check_restraint()

            # Commented because an 'if' is computationally expensive
            # sigma_x, sigma_y = np.std(self.particles[:, :2], axis=0)
            # self.sigma.append([self.dt * t, np.sqrt(sigma_x**2 + sigma_y**2)])

            self.sir[t] = [len(s), len(i), len(r), len(ns)]

            progress = int(50 * t / t_max)
            missing = int(50 - progress)
            print(f"0% [{'#'*progress}{' '*missing}] 100%", flush=True, end="\r")

        print(f"0% [{'#'*50}] 100%")

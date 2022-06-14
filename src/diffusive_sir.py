from typing import Union

import numpy as np
import matplotlib.pyplot as plt

from plot import plot_particles


class DiffusiveSIR(object):
    health_time = {}
    sigma = []
    sir = []
    confined_Time = {}

    D = 100  # m2/day
    dt = 0.01  # day
    recovery_time = 14.0  # day
    infected_distance = 2.0  # m
    infected_prob = 0.2
    confinement_time = 1.0  # day

    mapping = {
        0: "darkgreen",  # susceptible
        1: "darkred",  # infected
        2: "orange",  # recovered
        3: "blue",  # confined
    }

    def __init__(
        self,
        N: int,
        infected: float,
        density: float,
        confinement: Union[bool, float] = False,
    ):
        self.N = N
        self.L = np.sqrt(N / density)
        if confinement:
            self.L_conf = self.L * confinement
        else:
            self.L_conf = self.L

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

    @classmethod
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
            elif self.particles[i, 2] in (1, 3):
                infected.append(i)
                sick.append(i)
            else:
                recovered.append(i)
                sick.append(i)

        return susceptible, infected, recovered, sick

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

    def add_infected_time(self):
        for i in self.health_time:
            self.health_time[i] += self.dt

    def check_recovered(self):
        for i, v in list(self.health_time.items()):  # force copy of items
            if v >= self.recovery_time:
                self.particles[i, 2] = 2
                self.health_time.pop(i)
            elif v > self.confinement_time:
                self.particles[i, 2] = 3

    def add_confined_time(self):
        for i in self.confined_Time:
            self.confined_Time[i] += self.dt

    def evolve(self, t_max: int):
        sigma = 2.0 * self.D * self.dt
        const = np.sqrt(sigma) / np.sqrt(2)
        f_o = np.sqrt(2) * 0.348

        self.sir = np.zeros((t_max, 4))

        for t in range(t_max):
            # Move with periodic boundaries & confinement
            dx = f_o * const * np.random.normal(size=(self.N, 2))
            self.particles[:, :2] += dx
            for i in range(self.N):
                if self.particles[i, 2] != 3:
                    self.particles[i, :2] += self.L
                    self.particles[i, :2] %= self.L
                else:
                    self.particles[i, :2] += self.L_conf
                    self.particles[i, :2] %= self.L_conf

            s, i, r, ns = self.get_indices_by_health()

            self.check_infected(s, i)
            self.add_infected_time()
            self.check_recovered()

            self.sir[t] = [len(s), len(i), len(r), len(ns)]

            progress = int(50 * t / t_max)
            missing = int(50 - progress)
            print(f"0% [{'#'*progress}{' '*missing}] 100%", flush=True, end="\r")

        print(f"0% [{'#'*50}] 100%")

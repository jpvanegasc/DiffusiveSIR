import numpy as np
import matplotlib.pyplot as plt


def plot_circle(x: float, y: float):
    plt.scatter(x, y, color="black")


def plot_particles(particles: np.array, xlim=1, ylim=1):
    for p in particles:
        plot_circle(p[0], p[1])

    plt.xlim([0, xlim])
    plt.ylim([0, ylim])

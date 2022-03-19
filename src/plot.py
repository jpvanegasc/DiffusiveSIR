import numpy as np
import matplotlib.pyplot as plt


def plot_particles(particles: np.array, xlim=1, ylim=1, color=None):
    if isinstance(color, str):
        colors = [color for _ in particles]
    elif isinstance(color, list):
        colors = color
    else:
        colors = ["black" for _ in particles]

    for p_c in zip(particles, colors):
        p, c = p_c
        plt.scatter(p[0], p[1], color=c)

    plt.xlim([0, xlim])
    plt.ylim([0, ylim])

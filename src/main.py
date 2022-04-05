import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_particles


def main(N, t_max):
    d = DiffusiveSIR(N, 0.01, 0.012)

    colors = list(map(lambda h: d.get_health_color(h), d.particles[:, 2]))
    plot_particles(d.particles, d.L, d.L, color=colors)
    plt.savefig("../data/initial.png")
    plt.close()

    d.evolve(t_max)

    colors = list(map(lambda h: d.get_health_color(h), d.particles[:, 2]))
    plot_particles(d.particles, d.L, d.L, color=colors)
    plt.savefig("../data/final.png")
    plt.close()

    t = np.arange(t_max)

    plt.plot(t, d.sir[:, 0], color="green")
    plt.plot(t, d.sir[:, 1], color="red")
    plt.plot(t, d.sir[:, 2], color="yellow")
    plt.savefig("../data/sir.png")
    plt.close()


if __name__ == "__main__":
    main(1000, 1000)

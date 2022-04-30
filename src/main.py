import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_timestep
from plot import make_gif


def main(N, t_max):
    """N number of individuals, t_max in days"""
    d = DiffusiveSIR(N, 0.01, 0.012)

    t_max = int(t_max/d.dt)

    # Approx. map 100 to 30, 1000 to 20, 10000 to 10 and inf to 7
    marker_size = 23 * np.exp(-0.0005 * N) + 7

    plot_timestep(d, "../data/initial.png", "m", "m", "initial positions", marker_size)

    d.evolve(t_max)

    plot_timestep(d, "../data/final.png", "m", "m", "final positions", marker_size)

    #print("Wait a minute.... GIF in process...")
    #make_gif('../data/gif/' , '../data/spread.gif')

    t = d.dt * np.arange(t_max)

    plt.plot(t, d.sir[:, 0], color="darkgreen")
    plt.plot(t, d.sir[:, 1], color="darkred")
    plt.plot(t, d.sir[:, 2], color="orange")
    plt.plot(t, d.sir[:, 3], color="pink")
    plt.xlabel("$t$ (days)")
    plt.ylabel("Population")
    plt.savefig("../data/sir.png")
    plt.close()


if __name__ == "__main__":
    main(100, 45)

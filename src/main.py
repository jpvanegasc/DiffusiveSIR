import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_timestep



def main(N, t_max):
    """N number of individuals, t_max in days"""
    d = DiffusiveSIR(N, 0.01, 0.012)

    t_max = int(t_max/d.dt)

    # Approx. map 100 to 30, 1000 to 20, 10000 to 10 and inf to 7
    marker_size = 23 * np.exp(-0.0005 * N) + 7

    plot_timestep(d, "../data/initial.png", "m", "m", "initial positions", marker_size)

    d.evolve(t_max)

    plot_timestep(d, "../data/final.png", "m", "m", "final positions", marker_size)

    t = d.dt * np.arange(t_max)

    plt.plot(t, d.sir[:, 0], color="darkgreen")
    plt.plot(t, d.sir[:, 1], color="darkred")
    plt.plot(t, d.sir[:, 2], color="orange")
    plt.plot(t, d.sir[:,3],color="pink")
    plt.xlabel("$t$ (days)")
    plt.ylabel("Population")
    plt.savefig("../data/sir.png")
    plt.close()
    return d.sir, t

if __name__ == "__main__":
    sprom= np.zeros(9000)
    iprom= np.zeros(9000)
    rprom = np.zeros(9000)
    sickprom = np.zeros(9000)
    j = 10
    for i in range (j):
        x, y = main(100, 90)
        sprom += x[:,0]
        iprom += x[:,1]
        rprom += x[:,2]
        sickprom += x[:,3]
    sprom = sprom/j 
    iprom = iprom/j
    rprom = rprom/j
    sickprom = sickprom/j
    plt.plot(y,sprom, color = "black")
    plt.plot(y,iprom, color = "cyan")
    plt.plot(y,rprom, color = "magenta")
    plt.plot(y, sickprom, color ="green")
    plt.xlabel("$t$ días")
    plt.ylabel("Poblacion promedio")
    plt.savefig("../data/prom.png")
    plt.close()
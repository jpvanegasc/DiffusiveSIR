import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_particles


def main():
    d = DiffusiveSIR(100)
    
    plot_particles(d.particles, d.L, d.L)
    plt.scatter(5, 5, color="red")
    plt.savefig("initial.png")
    plt.close()

    d.evolve(100)

    plt.scatter(5, 5, color="red")
    plot_particles(d.particles, d.L, d.L)
    plt.savefig("final.png")
    plt.close()


if __name__ == "__main__":
    main()

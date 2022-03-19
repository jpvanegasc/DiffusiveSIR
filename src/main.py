import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_particles


def main():
    d = DiffusiveSIR(100, 20)

    colors = list(map(lambda h: d.get_health_color(h), d.health))
    plot_particles(d.particles, d.L, d.L, color=colors)
    # plt.scatter(5, 5, color="red")
    plt.savefig("initial.png")
    plt.close()

    d.evolve(100)

    colors = list(map(lambda h: d.get_health_color(h), d.health))
    plot_particles(d.particles, d.L, d.L, color=colors)
    plt.savefig("final.png")
    plt.close()


if __name__ == "__main__":
    main()

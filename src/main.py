import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_particles


def main():
    d = DiffusiveSIR(1000, 0.1, 0.012)

    colors = list(map(lambda h: d.get_health_color(h), d.health))
    plot_particles(d.particles, d.L, d.L, color=colors)
    plt.savefig("../data/initial.png")
    plt.close()

    d.evolve(1000)

    colors = list(map(lambda h: d.get_health_color(h), d.health))
    plot_particles(d.particles, d.L, d.L, color=colors)
    plt.savefig("../data/final.png")
    plt.close()

    plt.plot(d.healthy[:, 0], d.healthy[:, 1], color="green")
    plt.plot(d.sick[:, 0], d.sick[:, 1], color="red")
    plt.plot(d.recovered[:, 0], d.recovered[:, 1], color="yellow")
    plt.savefig("../data/sir.png")
    plt.close()


if __name__ == "__main__":
    main()

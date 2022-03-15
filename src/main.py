import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_circle


def main():
    d = DiffusiveSIR(1)

    for p in d.particles:
        plot_circle(d[0], p[1])

    plt.savefig("diffusion_results.py")
    plt.close()


if __name__ == "__main__":
    main()

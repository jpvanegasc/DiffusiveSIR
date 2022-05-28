import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_timestep, save_2d_array


def measure_sigma2(d: DiffusiveSIR, t_max: int, start: float = 0, end: float = None):
    """
    Measure variance for the system, starting in the origin.
    t_max, start and end must be in days.
    """
    from scipy import stats
    import scipy.optimize as opt

    linear = lambda x, a: a * x

    t_max = int(t_max / d.dt)
    sigma_start = int(start / d.dt)
    sigma_end = int(end / d.dt) if end else t_max

    d.measure_sigma2(t_max)

    c = opt.curve_fit(
        linear, d.sigma[sigma_start:sigma_end, 0], d.sigma[sigma_start:sigma_end, 1], 1
    )

    r = stats.linregress(
        d.sigma[sigma_start:sigma_end, 0], d.sigma[sigma_start:sigma_end, 1]
    )[2]

    save_2d_array(d.sigma, f"../data/sigma_D{d.D}.csv", header="t,sigma2")

    plt.plot(d.sigma[:, 0], d.sigma[:, 1], color="black")
    plt.plot(
        d.sigma[sigma_start:sigma_end, 0],
        linear(d.sigma[sigma_start:sigma_end, 0], c[0]),
        label=f"$\sigma^2={float(c[0]):.1f}t$\n$r^2={r**2:.4f}$",
        color="red",
    )
    plt.plot(
        d.sigma[sigma_start:sigma_end, 0],
        linear(d.sigma[sigma_start:sigma_end, 0], 2.0 * d.D),
        label=f"$\sigma^2=2D\:t$",
        color="darkgreen",
    )
    plt.legend()
    plt.xlabel(r"$t$")
    plt.ylabel(r"$\sigma^2$ (m)")
    plt.savefig(f"../data/sigma_D{d.D}.png")
    plt.close()


def main(N, t_max, sigma2=False):
    """Run the simulation. N number of individuals, t_max number of days"""
    d = DiffusiveSIR(N, 0.01, 0.012)

    #Approx. map 100 to 30, 1000 to 20, 10000 to 10 and inf to 7
    marker_size = 23 * np.exp(-0.0005 * N) + 7

    plot_timestep(d, "../data/initial.png", "m", "m", "initial positions", marker_size)

    t_max = int(t_max / d.dt)
    d.evolve(t_max)

    plot_timestep(d, "../data/final.png", "m", "m", "final positions", marker_size)

    # print("Wait a minute.... GIF in process...")
    # make_gif('../data/gif/' , '../data/spread.gif')

    t = d.dt * np.arange(t_max)

    plt.plot(t, d.sir[:, 0], color="darkgreen")
    plt.plot(t, d.sir[:, 1], color="darkred")
    plt.plot(t, d.sir[:, 2], color="orange")
    plt.plot(t, d.sir[:, 3], color="pink")
    plt.xlabel("$t$ (days)")
    plt.ylabel("Population")
    plt.savefig("../data/sir.png")
    plt.close()

    #if sigma2:
        # measure_sigma2(d, d.dt * t_max, end=7.5)


if __name__ == "__main__":
    main(100, 50, True)

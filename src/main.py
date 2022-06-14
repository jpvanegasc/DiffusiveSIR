import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR
from plot import plot_timestep, save_2d_array, LinearR

def main(N, t_max):
    """Run the simulation. N number of individuals, t_max number of days"""
    d = DiffusiveSIR(N, 0.01, 0.012, confinement=False)

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

    return d.sir , t

def average(N, t_max, ave):
    d = DiffusiveSIR(N, 0.01, 0.012)
    size = int (t_max / d.dt)
    sprom, iprom = np.zeros(size), np.zeros(size)
    rprom, sickprom = np.zeros(size), np.zeros(size)

    def indice(vec, max):
        for i in range (len(vec)):
            if vec[i] == max:
                s = i
                break
            else:
                continue
        return s

    for _ in range(ave):
        x, y = main(N, t_max)
        sprom += x[:, 0]
        iprom += x[:,1]
        rprom += x[:,2]
        sickprom += x[:,3]
    sprom, iprom = sprom / ave , iprom / ave
    rprom, sickprom = rprom / ave , sickprom / ave

    plt.figure(1)
    plt.plot(y,sprom, color = "black")
    plt.plot(y,iprom, color = "cyan")
    plt.plot(y,rprom, color = "magenta")
    plt.plot(y, sickprom, color ="green")
    plt.xlabel("$t$ días")
    plt.ylabel("Poblacion promedio")
    plt.savefig("../data/prom.png")
    plt.close()
    # plt.yscale("log")
    # fit (y,sickprom)
    max_sus = max(sprom)
    max_inf = max(sickprom)
    max_rec = max(rprom)
    max_enfer = max(iprom)

    a = indice(iprom, max_enfer)
    b = indice(sprom, max_sus)
    c = indice(rprom, max_rec)
    d = indice(sickprom, max_inf)
    # print (y[b],b)
    # print(y[d],d)
    # print(y[c],c)
    # print(y[a],a)
    Y = np.log(sickprom)
    coeff = LinearR(y[:501], Y[:501])
    m , b = coeff[2] , coeff[0]
    print("m = " , m , "b = ", b)
    plt.figure(2)
    plt.plot(y, Y, color = "green", label = 'Curva de infectados')
    plt.xlabel("$t$ días")
    plt.ylabel("Poblacion promedio")
    z = m * y[:501] + b
    m , b = str(m), str(b)
    plt.plot(y[:501], z, color = "red", label = "$s(t) =$ "+m[:m.find(".")+3]+"$*t + $" + b[:b.find(".")+3])
    plt.legend()
    plt.savefig("../data/fit.png")
    plt.close()


if __name__ == "__main__":
    average(100, 90 , 1)

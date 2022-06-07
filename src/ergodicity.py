import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR

def time_average_MSD(d, Nstep):
    r = np.random.randint(0, d.N)
    x_n = d.particles[r, :2]
    mu, sigma = 0.0, 2.0 * d.D * d.dt
    const = np.sqrt(sigma) / np.sqrt(2)
    msd = 0
    Path = np.zeros((Nstep, 2))

    for t in range(Nstep):
        Path[t] = d.particles[r, :2]
        dx = const * np.random.normal(size = 2)
        d.particles[r, :2] = np.absolute(d.particles[r, :2] + dx)
        if(d.particles[r, 0] >= d.L or d.particles[r, 1] >= d.L):
            d.particles[r, :2] -= 2 * dx

    for k in range(Nstep-1):
        norm = np.linalg.norm(Path[k+1] - Path[k])
        msd += norm ** 2

    tMSD = msd / Nstep
    return  tMSD, Path

def ensemble_average_MSD(d, Nstep):
    R0 = d.particles[:, :2].copy()
    mu, sigma = 0.0, 2.0 * d.D * d.dt
    const = np.sqrt(sigma) / np.sqrt(2)
    msd = 0

    for _ in range(Nstep):
        dx = const * np.random.normal(size=(d.N, 2))
        d.particles[:, :2] = np.absolute(d.particles[:, :2] + dx)
        for r in range(d.N):
            if(d.particles[r, 0] >= d.L or d.particles[r, 1] >= d.L):
                d.particles[r, :2] -= 2 * dx[r]
        
    RF = d.particles[:, :2]

    for ii in range(d.N):
        norm = np.linalg.norm(RF[ii] - R0[ii])
        msd += norm ** 2

    eMSD = msd / (d.N * Nstep)
    return eMSD , R0, RF

N = 100
d = DiffusiveSIR(N, 0.01, 0.012)
Nsteps = 10000
tMSD, Path = time_average_MSD(d, Nsteps)
eMSD, R0, RF  = ensemble_average_MSD(d, Nsteps) 
print(tMSD)
print(eMSD)
err = abs(tMSD - eMSD)/(tMSD)
print("error = ", err)

plt.figure(1)
plt.scatter(R0[:,0], R0[:,1],  color = "green" , label = 'Initial' )
plt.scatter(RF[:,0], RF[:,1], color = "red" , label = 'Final' )
plt.legend()

x0, xf = Path[0], Path[Nsteps - 1]
plt.figure(2)
plt.plot(Path[:, 0], Path[:, 1], color='cyan', label='Camino aleatorio')
plt.scatter(x0[0], x0[1], color = 'red' , label = "Posición inicial")
plt.scatter(xf[0], xf[1], color = 'green' , label = "Posición Final")
plt.legend()
plt.show()

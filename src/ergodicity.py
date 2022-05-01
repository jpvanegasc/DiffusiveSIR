import numpy as np
import matplotlib.pyplot as plt

from diffusive_sir import DiffusiveSIR

N = 100
d = DiffusiveSIR(N, 0.01, 0.012)

#def MSD():


def time_average_MSD(d, Nstep):
    X = d.particles[0,:2]
    dx, dy = 0, 0
    xn = X[0]
    yn = X[1]
    mu, sigma = 0.0, 2.0 * d.D * d.dt
    const = np.sqrt(sigma)
    Daniel = 2 * np.sqrt(np.pi)
    msd = 0
    RX , RY = [] , []

    for t in range(Nstep):
        RX.append(xn) , RY.append(yn)
        dx = const * np.random.normal(size = 1)*(1/Daniel)
        dy = const * np.random.normal(size = 1)*(1/Daniel)

        X[0] = abs( X[0] + dx)
        X[1] = abs( X[1] + dy)
        if(X[0] >= d.L): X[0] -= 2 * dx
        if(X[1] >= d.L): X[1] -= 2 * dy

        x_n1 , y_n1 = X[0] , X[1]
        msd += (x_n1-xn)**2 +(y_n1-yn)**2
        xn , yn = x_n1 , y_n1

    tMSD = msd / Nstep
    return tMSD , RX , RY

def ensemble_average_MSD(d, Nstep):
    X0 = d.particles[:, :2]
    X0 = np.array(X0)
    X = d.particles[:, :2],
    X = np.array(X)
    mu, sigma = 0.0, 2.0 * d.D * d.dt
    const = np.sqrt(sigma)
    Daniel = 2 * np.sqrt(np.pi)
    msd = 0

    for t in range(Nstep):
        dx = const * np.random.normal(size=(d.N, 2))*(1/Daniel)
        dx = np.array(dx)
        X[:,:] += dx

        if(X[:, 0] >= d.L).all(): X[kk][0] -= 2 * dx[kk][0]
        if(X[:, 1] >= d.L).all(): X[kk][1] -= 2 * dx[kk][1]

    XN = X[0]

    for ii in range(d.N):
        msd += ( XN[ii, 0] - X0[ii, 0] )**2 + ( XN[ii, 1] - X0[ii, 1] )**2

    eMSD = msd / (d.N * Nstep)
    return eMSD , X0, XN

# R0, RN = ensemble_average_MSD(d, 100)
# print("R0 = ", R0)
# print("RN = ", RN)

tMSD, RX, RY = time_average_MSD(d, 1000)
eMSD, R0, RN = ensemble_average_MSD(d, 1000)
print(tMSD)
print(eMSD)
err = abs(tMSD - eMSD)/(tMSD)
print("error = ", err)

plt.scatter(R0[:,0], R0[:,1],  color = "red" , label = 'Initial' )
plt.scatter(RN[:,0], RN[:,1], color = "green" , label = 'Final' )

plt.plot(RX, RY, color='cyan', label='Camino aleatorio')
plt.legend()
plt.show()

import numpy as np


class DiffusiveSIR(object):
    def __init__(self, N: int):
        self.N = N
        self.particles = np.zeros((N, 2))

    def run(self):
        pass

import numpy as np
import matplotlib.pyplot as plt
import os
import imageio as io

def plot_particles(particles: np.array, xlim=1, ylim=1, color=None, size=10):
    if isinstance(color, str):
        colors = [color for _ in particles]
    elif isinstance(color, list):
        colors = color
    else:
        colors = ["black" for _ in particles]

    for p_c in zip(particles, colors):
        p, c = p_c
        plt.scatter(p[0], p[1], color=c, s=size)

    plt.xlim([0, xlim])
    plt.ylim([0, ylim])


def plot_timestep(diffusive_sir, filename, xlabel="", ylabel="", title="", size=10):
    colors = list(
        map(lambda h: diffusive_sir.get_health_color(h), diffusive_sir.particles[:, 2])
    )
    plot_particles(
        diffusive_sir.particles,
        diffusive_sir.L,
        diffusive_sir.L,
        color=colors,
        size=size,
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    plt.close()

def save_2d_array(array: np.array, filename, header=None):
    with open(filename, "w+") as f:
        if header:
            f.write(header.strip() + "\n")
        for line in array:
            f.write(",".join(map(lambda x: str(x), line)) + "\n")

def make_gif(path, filename):
    # data base localization
    #path = path #path where the images are saved
    array_files = sorted(os.listdir(path))
    img_array = []

    #Read every file and save it into an list
    for x in range(0, len(array_files)):
        name_file = array_files[x]
        path_file = path + str(name_file)
        #print(path_file)
        #
        read_image = io.imread(path_file)
        img_array.append(read_image)

    #Save GIF
    io.mimwrite(filename, img_array, 'GIF', duration=0.1)

"""Plot state of system at init and boundary points: actual state given by user and calculated state."""


import numpy as np
import matplotlib.pyplot as plt

def ShowTheSolution(x, data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    i = 0
    colors = ['r', 'g']
    functions = ['approximation', 'actual y']
    for func in x:
        xs = [point[0] for point in data.i_points]
        ys = [point[1] for point in data.i_points]
        ts = [0 for point in data.i_points]
        zs = np.array([func(x, y, time) for x, y, time in zip(xs, ys, ts)])
        ax.scatter(xs, ys, zs, marker='o', color=colors[i % 2], label=functions[i % 2]+' at init points')
        i += 1
    for func in x:
        xs = [point[0] for point in data.b_points]
        ys = [point[1] for point in data.b_points]
        ts = [point[2] for point in data.b_points]
        zs = np.array([func(x, y, time) for x, y, time in zip(xs, ys, ts)])
        ax.scatter(xs, ys, zs, marker='x', color=colors[i % 2], label=functions[i % 2]+' at boundary points')
        i += 1
    ax.legend()
    plt.show()

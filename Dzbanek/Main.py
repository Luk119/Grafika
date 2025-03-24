import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import comb

matplotlib.use('MacOSX')  # Zmień na TkAgg, jeśli masz tkinter

def bernstein(n, i, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_patch(control_points):
    resolution = 20
    u_vals = np.linspace(0, 1, resolution)
    w_vals = np.linspace(0, 1, resolution)
    surface = []
    for u in u_vals:
        for w in w_vals:
            px, py, pz = 0.0, 0.0, 0.0
            for i in range(4):
                for j in range(4):
                    b_u = bernstein(3, i, u)
                    b_w = bernstein(3, j, w)
                    index = i * 4 + j
                    px += control_points[index][0] * b_u * b_w
                    py += control_points[index][1] * b_u * b_w
                    pz += control_points[index][2] * b_u * b_w
            surface.append([px, py, pz])
    return np.array(surface)

def plot_teapot(control_points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for k in range(control_points.shape[0]):
        surface = bezier_patch(control_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='b', alpha=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=30, azim=45)
    ax.set_box_aspect([1, 1, 1])
    plt.show(block=True)

def read_control_points_from_txt(file_path, shape):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    points = [list(map(float, line.split())) for line in lines if line.strip()]
    if len(points) != shape[0] * shape[1]:
        raise ValueError("Nieprawidłowa liczba punktów w pliku txt " + file_path)
    return np.array(points).reshape(shape)

file_path = "/Users/lukaszkundzicz/PycharmProjects/Grafika/Dzbanek/punkty.txt"
control_points = read_control_points_from_txt(file_path, (32, 16, 3))
print(control_points.shape)  # Sprawdzenie poprawności
plot_teapot(control_points)
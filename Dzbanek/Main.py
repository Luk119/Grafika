import numpy as np
import matplotlib.pyplot as plt
import matplotlib


# Ustawienie backendu interaktywnego
matplotlib.use('TkAgg')
plt.ion()


def bernstein(n, i, t):
    from math import comb
    return comb(n, i) * (t * i) * ((1 - t) * (n - i))


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
        ax.scatter(surface[:, 0], surface[:, 1], surface[:, 2], s=1, color='b')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=30, azim=45)  # Początkowy kąt widoku
    ax.set_box_aspect([1, 1, 1])  # Utrzymanie równych proporcji osi
    plt.show(block=True)  # Interaktywny widok umożliwiający obracanie myszką

import numpy as np

def read_control_points_from_txt(file_path, shape):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    points = [list(map(float, line.split())) for line in lines if line.strip()]
    if len(points) != shape[0] * shape[1]:
        raise ValueError("Nieprawidłowa liczba punktów w pliku txt " + file_path)
    return np.array(points).reshape(shape)
file_path = "Dzbanek/punkty.txt"  # Ścieżka do pliku z punktami
control_points = read_control_points_from_txt(file_path, (32, 16, 3))
plot_teapot(control_points)
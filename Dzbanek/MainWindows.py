import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from math import comb
# (Windows)
matplotlib.use('TkAgg')

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


def plot_objects(teacup_points, teapot_points, spoon_points, shift_x=4.0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Poprawiona orientacja filiżanki
    teacup_points = np.copy(teacup_points) * 1.5
    teacup_points[:, :, [1, 2]] = teacup_points[:, :, [2, 1]]  # Zamiana Y i Z
    teacup_points[:, :, 0] += shift_x  # Przesunięcie filiżanki obok dzbanka

    # Przesunięcie łyżki dla lepszego widoku
    spoon_points = np.copy(spoon_points) * 2
    spoon_points[:, :, 0] -= 2.0  # Przesunięcie w lewo

    # Rysowanie filiżanki
    for k in range(teacup_points.shape[0]):
        surface = bezier_patch(teacup_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='black', alpha=0.2)

    # Rysowanie dzbanka
    for k in range(teapot_points.shape[0]):
        surface = bezier_patch(teapot_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='navy', alpha=0.3)

    # Rysowanie łyżki
    for k in range(spoon_points.shape[0]):
        surface = bezier_patch(spoon_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='pink', alpha=0.6)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=30, azim=45)
    ax.set_box_aspect([1, 1, 1])
    plt.show()


def read_control_points_from_txt(file_path, shape):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    points = [list(map(float, line.split())) for line in lines if line.strip()]
    if len(points) != shape[0] * shape[1]:
        raise ValueError("Nieprawidłowa liczba punktów w pliku " + file_path)
    return np.array(points).reshape(shape)

# Wczytanie punktów kontrolnych dla filiżanki, dzbanka i łyżki(MacOs)
# teacup_file = "/Users/lukaszkundzicz/PycharmProjects/Grafika/Dzbanek/punkty2.txt"
# teapot_file = "/Users/lukaszkundzicz/PycharmProjects/Grafika/Dzbanek/punkty.txt"
# spoon_file = "/Users/lukaszkundzicz/PycharmProjects/Grafika/Dzbanek/punkty3.txt"

# (Windows)
teacup_file = "C:\Pythonik studia\Grafika\Dzbanek\punkty2.txt"
teapot_file = "C:\Pythonik studia\Grafika\Dzbanek\punkty.txt"
spoon_file = "C:\Pythonik studia\Grafika\Dzbanek\punkty3.txt"

teacup_points = read_control_points_from_txt(teacup_file, (26, 16, 3))
teapot_points = read_control_points_from_txt(teapot_file, (32, 16, 3))
spoon_points = read_control_points_from_txt(spoon_file, (16, 16, 3))

plot_objects(teacup_points, teapot_points, spoon_points)

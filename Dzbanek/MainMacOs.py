import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from math import comb

# ustawienie backendu matplotlib na macos
matplotlib.use('MacOSX')


def bernstein(n, i, t):
    # funkcja obliczająca wartość wielomianu bernsteina
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))


def bezier_patch(control_points):
    # tworzenie siatki punktów parametrycznych dla powierzchni béziera
    resolution = 20
    u_vals = np.linspace(0, 1, resolution)
    w_vals = np.linspace(0, 1, resolution)
    surface = []

    # iteracja po wartościach u i w w celu obliczenia współrzędnych x, y, z
    for u in u_vals:
        for w in w_vals:
            px, py, pz = 0.0, 0.0, 0.0

            # iteracja po punktach kontrolnych
            for i in range(4):
                for j in range(4):
                    b_u = bernstein(3, i, u)
                    b_w = bernstein(3, j, w)
                    index = i * 4 + j
                    px += control_points[index][0] * b_u * b_w
                    py += control_points[index][1] * b_u * b_w
                    pz += control_points[index][2] * b_u * b_w

            # dodanie obliczonego punktu do listy surface
            surface.append([px, py, pz])

    return np.array(surface)


def plot_objects(teacup_points, teapot_points, spoon_points, shift_x=4.0):
    # tworzenie figury i osi 3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # poprawiona orientacja filiżanki
    teacup_points = np.copy(teacup_points) * 1.5
    teacup_points[:, :, [1, 2]] = teacup_points[:, :, [2, 1]]  # zamiana y i z
    teacup_points[:, :, 0] += shift_x  # przesunięcie filiżanki obok dzbanka

    # przesunięcie łyżki dla lepszego widoku
    spoon_points = np.copy(spoon_points) * 2
    spoon_points[:, :, 0] -= 2.0  # przesunięcie w lewo

    # rysowanie filiżanki
    for k in range(teacup_points.shape[0]):
        surface = bezier_patch(teacup_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='black', alpha=0.2)

    # rysowanie dzbanka
    for k in range(teapot_points.shape[0]):
        surface = bezier_patch(teapot_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='navy', alpha=0.3)

    # rysowanie łyżki
    for k in range(spoon_points.shape[0]):
        surface = bezier_patch(spoon_points[k])
        ax.plot_trisurf(surface[:, 0], surface[:, 1], surface[:, 2], color='pink', alpha=0.6)

    # ustawienia wykresu
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=30, azim=45)
    ax.set_box_aspect([1, 1, 1])
    plt.show()


def read_control_points_from_txt(file_path, shape):
    # wczytywanie punktów kontrolnych z pliku tekstowego
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # konwersja danych do listy liczb zmiennoprzecinkowych
    points = [list(map(float, line.split())) for line in lines if line.strip()]

    # sprawdzenie poprawności liczby punktów
    if len(points) != shape[0] * shape[1]:
        raise ValueError("nieprawidłowa liczba punktów w pliku " + file_path)

    return np.array(points).reshape(shape)


# ścieżki do plików zawierających punkty kontrolne (macos)
teapot_file = "punkty.txt"
teacup_file = "punkty2.txt"
spoon_file = "punkty3.txt"

# (windows)
# teacup_file = "C:\\Pythonik studia\\Grafika\\Dzbanek\\punkty2.txt"
# teapot_file = "C:\\Pythonik studia\\Grafika\\Dzbanek\\punkty.txt"
# spoon_file = "C:\\Pythonik studia\\Grafika\\Dzbanek\\punkty3.txt"

# wczytanie punktów
teacup_points = read_control_points_from_txt(teacup_file, (26, 16, 3))
teapot_points = read_control_points_from_txt(teapot_file, (32, 16, 3))
spoon_points = read_control_points_from_txt(spoon_file, (16, 16, 3))

# rysowanie
plot_objects(teacup_points, teapot_points, spoon_points)

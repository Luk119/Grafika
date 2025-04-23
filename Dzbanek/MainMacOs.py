import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from math import comb

matplotlib.use('MacOSX')

# Funkcja Bernsteina
def bernstein(n, i, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

# Funkcja generująca powierzchnię Béziera na podstawie punktów kontrolnych
def bezier_patch(control_points):
    # Tworzenie siatki punktów
    resolution = 20
    u_vals = np.linspace(0, 1, resolution)
    w_vals = np.linspace(0, 1, resolution)
    surface = []

    # Iteracja po wartościach u i w, obliczanie współrzędnych x, y, z
    for u in u_vals:
        for w in w_vals:
            px, py, pz = 0.0, 0.0, 0.0

            # Iteracja po punktach kontrolnych
            for i in range(4):
                for j in range(4):
                    b_u = bernstein(3, i, u)
                    b_w = bernstein(3, j, w)
                    index = i * 4 + j
                    px += control_points[index][0] * b_u * b_w
                    py += control_points[index][1] * b_u * b_w
                    pz += control_points[index][2] * b_u * b_w

            # Dodanie obliczonego punktu do listy surface
            surface.append([px, py, pz])

    return np.array(surface)

# Funkcja do rysowania obiektów 3D
def plot_objects(teacup_points, teapot_points, spoon_points, shift_x=4.0):
    # Tworzenie figury i osi 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Poprawiona orientacja filiżanki
    teacup_points = np.copy(teacup_points) * 1.5
    teacup_points[:, :, [1, 2]] = teacup_points[:, :, [2, 1]]  # Zamiana y i z
    teacup_points[:, :, 0] += shift_x

    # Przesunięcie łyżki dla lepszego widoku
    spoon_points = np.copy(spoon_points) * 2
    spoon_points[:, :, 0] -= 2.0

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

    # Ustawienia wykresu
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=30, azim=45)
    ax.set_box_aspect([1, 1, 1])  # Ustawienie proporcji osi
    plt.show()

# Funkcja do wczytywania punktów kontrolnych z pliku tekstowego
def read_control_points_from_txt(file_path, shape):
    # Wczytywanie punktów kontrolnych z pliku
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Konwersja danych do listy liczb zmiennoprzecinkowych
    points = [list(map(float, line.split())) for line in lines if line.strip()]

    # Sprawdzenie poprawności liczby punktów
    if len(points) != shape[0] * shape[1]:
        raise ValueError("Nieprawidłowa liczba punktów w pliku " + file_path)

    return np.array(points).reshape(shape)

# Wczytywanie punktów kontrolnych z plików
teapot_file = "punkty.txt"
teacup_file = "punkty2.txt"
spoon_file = "punkty3.txt"

# Wczytanie punktów
teacup_points = read_control_points_from_txt(teacup_file, (26, 16, 3))
teapot_points = read_control_points_from_txt(teapot_file, (32, 16, 3))
spoon_points = read_control_points_from_txt(spoon_file, (16, 16, 3))

# Rysowanie obiektów
plot_objects(teacup_points, teapot_points, spoon_points)

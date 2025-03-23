import numpy as np
from PIL import Image, ImageDraw


# Funkcja do obliczania punktów krzywej Béziera
def bezier_curve(p0, p1, p2, p3, t):
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return (x, y)


# Funkcja rysująca krzywe na obrazie
def draw_curves(curves, filename, color='black'):
    width, height = 500, 450
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    for points in curves:
        p0, p1, p2, p3 = points
        curve_points = [(int(bezier_curve(p0, p1, p2, p3, t)[0]), int(bezier_curve(p0, p1, p2, p3, t)[1])) for t in
                        np.linspace(0, 1, 100)]

        # Rysowanie krzywej Béziera
        draw.line(curve_points, fill=color, width=2)

        # Rysowanie linii pomocniczych do punktów kontrolnych
        draw.line([tuple(p0), tuple(p1)], fill='gray', width=1)
        draw.line([tuple(p0), tuple(p2)], fill='gray', width=1)

        # Rysowanie punktów kontrolnych
        for p in [p1, p2, p3]:
            draw.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill='black')

        # Rysowanie głównych punktów początkowych (na czerwono)
        draw.ellipse([p0[0] - 5, p0[1] - 5, p0[0] + 5, p0[1] + 5], fill='red')

    img.show()
    img.save(filename)


# Krzywe dla litery "Ł"
curves_L = [
    [[224, 139], [205, 229], [190, 328], [176, 324]],
    [[176, 324], [85, 299], [231, 409], [202, 350]],
    [[202, 350], [189, 323], [337, 339], [347, 353]],
    [[347, 353], [400, 429], [350, 223], [329, 305]],
    [[329, 305], [325, 321], [225, 295], [222, 310]],
    [[222, 310], [219, 324], [230, 259], [235, 258]],
    [[235, 258], [245, 256], [287, 253], [292, 258]],
    [[292, 258], [346, 308], [305, 142], [288, 207]],
    [[288, 207], [284, 222], [238, 233], [238, 232]],
    [[238, 232], [254, 167], [255, 144], [268, 137]],
    [[268, 137], [346, 98], [167, 104], [225, 138]],
]


# Krzywe dla litery "K"
curves_K = [
    [[200, 100], [90, 50], [350, 45], [240, 105]],
    [[240, 105], [230, 115], [255, 170], [240, 185]],
    [[240, 185], [225, 195], [310, 130], [310, 105]],
    [[310, 105], [290, 10], [460, 150], [350, 140]],
    [[350, 140], [340, 135], [270, 230], [265, 210]],
    [[265, 210], [290, 190], [300, 320], [370, 350]],
    [[370, 350], [440, 380], [230, 400], [310, 360]],
    [[310, 360], [320, 350], [250, 270], [240, 255]],
    [[240, 255], [230, 240], [220, 350], [230, 360]],
    [[230, 360], [320, 400], [80, 420], [170, 360]],
    [[170, 360], [230, 330], [200, 100], [200, 100]],
]

# Rysowanie i zapisywanie dwóch oddzielnych obrazów
draw_curves(curves_L, "litera_L.png", color='black')
draw_curves(curves_K, "litera_K.png", color='black')

from PIL import Image, ImageFilter
import numpy as np
import matplotlib.pyplot as plt


def load_image(path):
    img = Image.open(path).convert('RGB')
    return img

def save_image(img, path):
    img.save(path)

def show_menu():
    print("\n--- MENU ---")
    print("1. Transformacja liniowa (rozjaśnianie, przyciemnianie, negatyw)")
    print("2. Transformacja potęgowa (rozjaśnianie, przyciemnianie)")
    print("3. Mieszanie dwóch obrazów (16 trybów)")
    print("4. Modyfikacja kontrastu")
    print("5. Generowanie histogramu R, G, B")
    print("6. Wyrównywanie histogramu")
    print("7. Skalowanie histogramu")
    print("8. Filtr dolnoprzepustowy")
    print("9. Filtry górnoprzepustowe (Roberts, Prewitt, Sobel, Laplace)")
    print("10. Filtry statystyczne (min, max, medianowy)")
    print("0. Wyjście")

# --- Transformacje liniowe ---
def brighten(img, value):
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = min(255, r + value)
            g = min(255, g + value)
            b = min(255, b + value)
            result.putpixel((i, j), (r, g, b))
    return result

def darken(img, value):
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r = max(0, r - value)
            g = max(0, g - value)
            b = max(0, b - value)
            result.putpixel((i, j), (r, g, b))
    return result

def negative(img):
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            result.putpixel((i, j), (255 - r, 255 - g, 255 - b))
    return result

# --- Transformacja potęgowa ---
def power_transform(img, c, n):
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r_norm = r / 255.0
            g_norm = g / 255.0
            b_norm = b / 255.0

            r_new = c * (r_norm ** n)
            g_new = c * (g_norm ** n)
            b_new = c * (b_norm ** n)

            r_new = min(255, max(0, int(r_new * 255)))
            g_new = min(255, max(0, int(g_new * 255)))
            b_new = min(255, max(0, int(b_new * 255)))

            result.putpixel((i, j), (r_new, g_new, b_new))
    return result

# --- Mieszanie obrazów ---
def blend_images(img1, img2, mode, alpha=0.5):
    w, h = img1.size
    if img2.size != (w, h):
        img2 = img2.resize((w, h))

    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r1, g1, b1 = img1.getpixel((i, j))
            r2, g2, b2 = img2.getpixel((i, j))

            r = blend_mode(r1, r2, mode, alpha)
            g = blend_mode(g1, g2, mode, alpha)
            b = blend_mode(b1, b2, mode, alpha)

            result.putpixel((i, j), (r, g, b))
    return result

def blend_mode(a, b, mode, alpha):
    a /= 255.0
    b /= 255.0
    if mode == 1: res = min(1, a + b)
    elif mode == 2: res = max(0, min(1, a + b - 1))
    elif mode == 3: res = abs(a - b)
    elif mode == 4: res = a * b
    elif mode == 5: res = 1 - (1 - a) * (1 - b)
    elif mode == 6: res = 1 - abs(1 - a - b)
    elif mode == 7: res = min(a, b)
    elif mode == 8: res = max(a, b)
    elif mode == 9: res = a + b - 2 * a * b
    elif mode == 10: res = 2 * a * b if a < 0.5 else 1 - 2 * (1 - a) * (1 - b)
    elif mode == 11: res = 2 * a * b if b < 0.5 else 1 - 2 * (1 - a) * (1 - b)
    elif mode == 12:
        if b < 0.5:
            res = 2 * a * b + a * a * (1 - 2 * b)
        else:
            res = np.sqrt(a) * (2 * b - 1) + 2 * a * (1 - b)
    elif mode == 13: res = min(1, a / (1 - b)) if (1 - b) != 0 else 1
    elif mode == 14: res = max(0, 1 - (1 - a) / b) if b != 0 else 0
    elif mode == 15: res = min(1, a * a / (1 - b)) if (1 - b) != 0 else 1
    elif mode == 16: res = (1 - alpha) * b + alpha * a
    else: res = a
    return int(min(255, max(0, res * 255)))

# --- Kontrast ---
def adjust_contrast(img, factor):
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))

            r = int((r - 128) * factor + 128)
            g = int((g - 128) * factor + 128)
            b = int((b - 128) * factor + 128)

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            result.putpixel((i, j), (r, g, b))
    return result

# --- Histogram ---
def generate_histogram(img):
    w, h = img.size
    hist_r = [0] * 256
    hist_g = [0] * 256
    hist_b = [0] * 256

    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            hist_r[r] += 1
            hist_g[g] += 1
            hist_b[b] += 1

    return hist_r, hist_g, hist_b

def equalize_histogram(img):
    w, h = img.size
    hist_r, hist_g, hist_b = generate_histogram(img)

    num_pixels = w * h

    cdf_r = [sum(hist_r[:i+1]) for i in range(256)]
    cdf_g = [sum(hist_g[:i+1]) for i in range(256)]
    cdf_b = [sum(hist_b[:i+1]) for i in range(256)]

    map_r = [int(255 * cdf_r[i] / num_pixels) for i in range(256)]
    map_g = [int(255 * cdf_g[i] / num_pixels) for i in range(256)]
    map_b = [int(255 * cdf_b[i] / num_pixels) for i in range(256)]

    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            r_eq = map_r[r]
            g_eq = map_g[g]
            b_eq = map_b[b]
            result.putpixel((i, j), (r_eq, g_eq, b_eq))

    return result

def scale_histogram(img, min_val, max_val):
    w, h = img.size
    result = Image.new('RGB', (w, h))
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))

            r_new = int((r - min_val) * 255 / (max_val - min_val))
            g_new = int((g - min_val) * 255 / (max_val - min_val))
            b_new = int((b - min_val) * 255 / (max_val - min_val))

            r_new = max(0, min(255, r_new))
            g_new = max(0, min(255, g_new))
            b_new = max(0, min(255, b_new))

            result.putpixel((i, j), (r_new, g_new, b_new))
    return result

# --- Filtry ---
def low_pass_filter(img):
    return img.filter(ImageFilter.GaussianBlur(radius=2))

# --- Main program ---
def main():
    print("Wczytaj obraz:")
    image_path = input("Podaj ścieżkę do pliku: ")
    img = load_image(image_path)

    while True:
        show_menu()
        choice = int(input("Wybierz opcję: "))
        if choice == 1:
            print("1. Rozjaśnianie")
            value = int(input("Podaj wartość rozjaśnienia: "))
            result = brighten(img, value)
            save_image(result, "output_brightened.jpg")
            print("Obraz zapisany jako output_brightened.jpg")
        elif choice == 2:
            print("2. Transformacja potęgowa")
            c = float(input("Podaj wartość c: "))
            n = float(input("Podaj wartość n: "))
            result = power_transform(img, c, n)
            save_image(result, "output_power_transformed.jpg")
            print("Obraz zapisany jako output_power_transformed.jpg")
        elif choice == 3:
            print("3. Mieszanie obrazów")
            image_path2 = input("Podaj ścieżkę do drugiego obrazu: ")
            img2 = load_image(image_path2)
            print("Wybierz tryb mieszania:")
            print("1. Additive")
            print("2. Subtractive")
            print("3. Difference")
            print("4. Multiply")
            mode = int(input("Podaj numer trybu: "))
            alpha = float(input("Podaj wartość alpha (0-1): "))
            result = blend_images(img, img2, mode, alpha)
            save_image(result, "output_blended.jpg")
            print("Obraz zapisany jako output_blended.jpg")
        elif choice == 4:
            factor = float(input("Podaj wartość czynnika kontrastu: "))
            result = adjust_contrast(img, factor)
            save_image(result, "output_contrast_adjusted.jpg")
            print("Obraz zapisany jako output_contrast_adjusted.jpg")
        elif choice == 5:
            hist_r, hist_g, hist_b = generate_histogram(img)
            plt.plot(hist_r, color="red", label="Czerwony")
            plt.plot(hist_g, color="green", label="Zielony")
            plt.plot(hist_b, color="blue", label="Niebieski")
            plt.legend()
            plt.show()
        elif choice == 6:
            result = equalize_histogram(img)
            save_image(result, "output_equalized.jpg")
            print("Obraz zapisany jako output_equalized.jpg")
        elif choice == 7:
            min_val = int(input("Podaj wartość minimalną: "))
            max_val = int(input("Podaj wartość maksymalną: "))
            result = scale_histogram(img, min_val, max_val)
            save_image(result, "output_scaled.jpg")
            print("Obraz zapisany jako output_scaled.jpg")
        elif choice == 8:
            result = low_pass_filter(img)
            save_image(result, "output_low_pass_filtered.jpg")
            print("Obraz zapisany jako output_low_pass_filtered.jpg")
        elif choice == 0:
            break
        else:
            print("Niepoprawna opcja")

if __name__ == "__main__":
    main()

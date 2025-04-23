import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
from scipy import ndimage


class SimpleImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGB")
        self.array = np.array(self.image)

    def show(self, img=None, title="Obraz", cmap=None):
        if img is None:
            plt.imshow(self.array)
        else:
            if isinstance(img, np.ndarray):
                plt.imshow(img, cmap=cmap)
            else:  # jeśli to PIL Image
                plt.imshow(np.array(img), cmap=cmap)
        plt.title(title)
        plt.axis('off')
        plt.show()

    # ===== Transformacje liniowe =====
    def brighten(self, value=50):
        """Rozjaśnianie obrazu"""
        brightened = np.clip(self.array.astype(int) + value, 0, 255).astype(np.uint8)
        self.show(brightened, f"Rozjaśniony (+{value})")
        return brightened

    def darken(self, value=50):
        """Przyciemnianie obrazu"""
        darkened = np.clip(self.array.astype(int) - value, 0, 255).astype(np.uint8)
        self.show(darkened, f"Przyciemniony (-{value})")
        return darkened

    def negative(self):
        """Negatyw obrazu"""
        neg = 255 - self.array
        self.show(neg, "Negatyw")
        return neg

    # ===== Transformacja potęgowa (gamma) =====
    def gamma_correction(self, gamma=1.0):
        """Korekcja gamma"""
        normalized = self.array / 255.0
        corrected = np.power(normalized, gamma) * 255
        corrected = corrected.astype(np.uint8)
        self.show(corrected, f"Gamma (γ={gamma})")
        return corrected

    # ===== Mieszanie obrazów =====
    def blend(self, other_img_path, alpha=0.5):
        """Mieszanie dwóch obrazów (alpha-blending)"""
        other_img = np.array(Image.open(other_img_path).convert("RGB"))

        # Dopasowanie rozmiarów
        h, w = self.array.shape[:2]
        other_img = np.array(Image.fromarray(other_img).resize((w, h)))

        blended = (alpha * self.array + (1 - alpha) * other_img).astype(np.uint8)
        self.show(blended, f"Alpha blending (α={alpha})")
        return blended

    # ===== Kontrast =====
    def adjust_contrast(self, factor=1.5):
        """Regulacja kontrastu"""
        enhancer = ImageEnhance.Contrast(self.image)
        contrasted = enhancer.enhance(factor)
        self.show(contrasted, f"Kontrast (wsp. {factor})")
        return np.array(contrasted)

    # ===== Histogram =====
    def show_histogram(self):
        """Wyświetla histogram RGB"""
        plt.figure(figsize=(10, 4))
        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            hist, _ = np.histogram(self.array[:, :, i], bins=256, range=(0, 256))
            plt.plot(hist, color=color)
        plt.title("Histogram RGB")
        plt.xlabel("Wartość piksela")
        plt.ylabel("Liczba pikseli")
        plt.show()

    # ===== Filtry dolnoprzepustowe (rozmycie) =====
    def blur(self, radius=2):
        """Rozmycie Gaussa (uproszczone)"""
        blurred = self.image.filter(ImageFilter.GaussianBlur(radius))
        self.show(blurred, f"Rozmycie (r={radius})")
        return np.array(blurred)

    # ===== Filtry górnoprzepustowe (krawędzie) =====
    def edge_detection(self, mode="sobel"):
        """Wykrywanie krawędzi (Sobel, Prewitt, Roberts)"""
        gray = np.array(self.image.convert("L"))  # Konwersja do skali szarości

        if mode == "sobel":
            kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        elif mode == "prewitt":
            kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
            kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        elif mode == "roberts":
            kernel_x = np.array([[1, 0], [0, -1]])
            kernel_y = np.array([[0, 1], [-1, 0]])
        else:
            raise ValueError("Dostępne tryby: 'sobel', 'prewitt', 'roberts'")

        # Konwolucja z kernelami
        grad_x = ndimage.convolve(gray, kernel_x)
        grad_y = ndimage.convolve(gray, kernel_y)
        edges = np.sqrt(grad_x ** 2 + grad_y ** 2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        self.show(edges, f"Krawędzie ({mode})", cmap="gray")
        return edges

    # ===== Filtry statystyczne =====
    def median_filter(self, size=3):
        """Filtr medianowy"""
        filtered = self.image.filter(ImageFilter.MedianFilter(size))
        self.show(filtered, f"Filtr medianowy ({size}x{size})")
        return np.array(filtered)


# Przykład użycia
if __name__ == "__main__":
    processor = SimpleImageProcessor("images.jpeg")
    processor.show(title="Oryginał")

    # Transformacje liniowe
    processor.brighten(50)
    processor.darken(50)
    processor.negative()

    # Transformacja gamma
    processor.gamma_correction(0.5)  # Rozjaśnianie
    processor.gamma_correction(1.5)  # Przyciemnianie

    # Mieszanie obrazów (wymaga drugiego obrazu)
    # processor.blend("drugi_obraz.jpg", alpha=0.7)

    # Kontrast
    processor.adjust_contrast(1.5)

    # Histogram
    processor.show_histogram()

    # Filtry dolnoprzepustowe
    processor.blur(radius=2)

    # Filtry górnoprzepustowe (krawędzie)
    processor.edge_detection("sobel")
    processor.edge_detection("prewitt")
    processor.edge_detection("roberts")

    # Filtr medianowy
    processor.median_filter(3)
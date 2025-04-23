# ładowanie obrazów
import pygame  # import biblioteki pygame

def load_image(path, scale=1):  # funkcja do ładowania obrazu z opcjonalnym skalowaniem
    try:
        img = pygame.image.load(path).convert_alpha()  # ładuje obraz i konwertuje go z przezroczystością
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))  # zwraca przeskalowany obraz
    except pygame.error as e:  # obsługa błędów, jeśli obraz się nie załaduje
        print(f"błąd ładowania obrazu: {path}")  # informacja o problemie z ładowaniem
        print(f"błąd: {e}")  # wypisanie szczegółów błędu
        surf = pygame.Surface((50, 80), pygame.SRCALPHA)  # tworzy tymczasową powierzchnię z przezroczystością
        pygame.draw.rect(surf, (255, 0, 0, 128), (0, 0, 50, 80))  # rysuje czerwony półprzezroczysty prostokąt jako zastępstwo
        return surf  # zwraca tymczasowy obrazek jako rezerwę

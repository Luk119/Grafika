# Ładowanie obrazów
import pygame

def load_image(path, scale=1):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    except pygame.error as e:
        print(f"Błąd ładowania obrazu: {path}")
        print(f"Błąd: {e}")
        surf = pygame.Surface((50, 80), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0, 128), (0, 0, 50, 80))
        return surf

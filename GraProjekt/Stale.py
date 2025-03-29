# Inicjalizacja PyGame
import pygame

pygame.init()

# Ustawienia ekranu
SZEROKOSC = 1824
WYSOKOSC = 1200
WYSOKOSC_PODLOGI = 1000
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Elvis Szczurołap")

# Kolory
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
ZIELONY = (40, 150, 70)
CZERWONY = (220, 30, 30)

# Czcionka
czcionka = pygame.font.SysFont('Arial', 36)
duza_czcionka = pygame.font.SysFont('Arial', 72)
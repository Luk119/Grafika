# Stałe wartości w grze
import pygame
pygame.init()

SZEROKOSC = 1124
WYSOKOSC = 800
WYSOKOSC_PODLOGI = 700
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Elvis Szczurołap")

CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
ZIELONY = (40, 150, 70)
CZERWONY = (220, 30, 30)

czcionka = pygame.font.SysFont('Arial', 36)
duza_czcionka = pygame.font.SysFont('Arial', 72)
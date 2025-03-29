# Klasa Przeciwnika
from LoadImage import *
from Stale import *


class Przeciwnik(pygame.sprite.Sprite):
    def __init__(self, x, wysokosc_podlogi, predkosc):
        super().__init__()
        self.animacje = [
            load_image("enemy1.png"),
            load_image("enemy2.png")
        ]
        self.klatka_animacji = 0
        self.czas_animacji = 0
        self.image = self.animacje[self.klatka_animacji]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = wysokosc_podlogi
        self.predkosc = predkosc
        self.kierunek = 1

    def update(self):
        self.rect.x += self.predkosc * self.kierunek

        if self.rect.x <= 0 or self.rect.x >= SZEROKOSC - self.rect.width:
            self.kierunek *= -1
            self.image = pygame.transform.flip(self.image, True, False)

        self.czas_animacji += 1
        if self.czas_animacji >= 15:
            self.czas_animacji = 0
            self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje)
            self.image = self.animacje[self.klatka_animacji]

            if self.kierunek == 1:
                self.image = pygame.transform.flip(self.image, True, False)
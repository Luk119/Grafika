# klasa przeciwnika
from LoadImage import *  # importuje funkcję do ładowania obrazów
from Stale import *  # importuje stałe jak szerokość ekranu

class Przeciwnik(pygame.sprite.Sprite):  # dziedziczy po klasie Sprite z pygame
    def __init__(self, x, wysokosc_podlogi, predkosc):  # konstruktor przeciwnika
        super().__init__()  # wywołanie konstruktora klasy nadrzędnej
        self.animacje = [  # lista klatek animacji przeciwnika
            load_image("gameImages/enemy1.png"),
            load_image("gameImages/enemy2.png")
        ]
        self.klatka_animacji = 0  # indeks aktualnej klatki animacji
        self.czas_animacji = 0  # licznik czasu do zmiany klatki
        self.image = self.animacje[self.klatka_animacji]  # ustawienie początkowego obrazka
        self.rect = self.image.get_rect()  # pobranie prostokąta (pozycji) sprite’a
        self.rect.x = x  # ustawienie pozycji x
        self.rect.bottom = wysokosc_podlogi  # ustawienie dolnej krawędzi przeciwnika
        self.predkosc = predkosc  # prędkość poruszania się
        self.kierunek = 1  # kierunek poruszania się (1 = prawo, -1 = lewo)

    def update(self):  # metoda aktualizująca stan przeciwnika w każdej klatce gry
        self.rect.x += self.predkosc * self.kierunek  # przesuń przeciwnika

        if self.rect.x <= 0 or self.rect.x >= SZEROKOSC - self.rect.width:  # odbicie od krawędzi ekranu
            self.kierunek *= -1  # zmień kierunek
            self.image = pygame.transform.flip(self.image, True, False)  # odwróć obraz poziomo

        self.czas_animacji += 1  # zliczanie czasu animacji
        if self.czas_animacji >= 15:  # zmiana klatki animacji co 15 klatek
            self.czas_animacji = 0
            self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje)  # przełącz na następną klatkę
            self.image = self.animacje[self.klatka_animacji]  # ustaw nowy obraz

            if self.kierunek == 1:  # jeśli przeciwnik idzie w prawo
                self.image = pygame.transform.flip(self.image, True, False)  # odwróć obraz w prawo

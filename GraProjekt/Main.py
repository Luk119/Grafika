import pygame
import os
import sys

# Inicjalizacja PyGame
pygame.init()

# Ustawienia ekranu
SZEROKOSC = 1824
WYSOKOSC = 1200
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Prosta RPG")

# Kolory
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)

# Ładowanie grafik
def load_image(path, scale=1):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    except:
        print(f"Błąd ładowania obrazu: {path}")
        # Tworzenie zastępczego obrazu jeśli plik nie istnieje
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, 50, 50))
        return surf

# Klasa Gracza
class Gracz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animacje = {
            "idle": [load_image("playerIdle.png")],
            "run": [load_image("playerIdle.png")],
            "jump": [load_image("playerJump.png")],
            "attack": [load_image("img.png")],
            "shoot": [load_image("img.png")],
        }
        self.obecna_animacja = "idle"
        self.image = self.animacje[self.obecna_animacja][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.predkosc = 5
        self.skok = False
        self.sila_skoku = 20
        self.grawitacja = 0.3
        self.vel_y = 0
        self.kierunek = 1
        self.czas_skoku = 0  # Licznik czasu skoku
        self.czas_trwania_skoku = 30  # Klatki animacji skoku (około 0.5 sekundy przy 60 FPS)

    def update(self):
        # Poruszanie
        keys = pygame.key.get_pressed()

        # Jeśli nie jesteśmy w trakcie skoku, pozwalamy na zmianę animacji
        if not self.skok or self.czas_skoku <= 0:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.predkosc
                self.kierunek = -1
                self.obecna_animacja = "run"
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.predkosc
                self.kierunek = 1
                self.obecna_animacja = "run"
            else:
                self.obecna_animacja = "idle"

        # Skok
        if keys[pygame.K_SPACE] and not self.skok:
            self.vel_y = -self.sila_skoku
            self.skok = True
            self.obecna_animacja = "jump"
            self.czas_skoku = self.czas_trwania_skoku  # Ustawiamy czas trwania skoku

        # Zmniejszamy licznik czasu skoku
        if self.czas_skoku > 0:
            self.czas_skoku -= 1
            self.obecna_animacja = "jump"  # Wymuszamy animację skoku

        # Atak (mieczem) - tylko jeśli nie skaczemy
        if keys[pygame.K_z] and not self.skok:
            self.obecna_animacja = "attack"

        # Strzał (pocisk) - tylko jeśli nie skaczemy
        if keys[pygame.K_x] and not self.skok:
            self.obecna_animacja = "shoot"

        # Grawitacja
        self.vel_y += self.grawitacja
        self.rect.y += self.vel_y

        # Sprawdź kolizję z podłożem
        if self.rect.y >= WYSOKOSC - 100:
            self.rect.y = WYSOKOSC - 100
            self.skok = False
            self.vel_y = 0
            self.czas_skoku = 0  # Resetujemy czas skoku po wylądowaniu

        # Aktualizacja obrazu
        self.image = self.animacje[self.obecna_animacja][0]
        if self.kierunek == -1:
            self.image = pygame.transform.flip(self.image, True, False)

# Klasa Przeciwnika
class Przeciwnik(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animacje = {
            "run": [load_image("img.png")],
            "death": [load_image("img.png")],
        }
        self.obecna_animacja = "run"
        self.image = self.animacje[self.obecna_animacja][0]  # Zmiana z self.obraz na self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.predkosc = 2
        self.kierunek = 1

    def update(self):
        # Poruszanie się przeciwnika
        self.rect.x += self.predkosc * self.kierunek
        if self.rect.x <= 0 or self.rect.x >= SZEROKOSC - 50:
            self.kierunek *= -1
            self.image = pygame.transform.flip(self.image, True, False)

# Klasa Pocisku
class Pocisk(pygame.sprite.Sprite):
    def __init__(self, x, y, kierunek):
        super().__init__()
        self.image = load_image("img.png", 0.1)  # Zmiana z self.obraz na self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kierunek = kierunek
        self.predkosc = 7

    def update(self):
        self.rect.x += self.predkosc * self.kierunek
        if self.rect.x < 0 or self.rect.x > SZEROKOSC:
            self.kill()

# Główna pętla gry
def main():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    przeciwnicy = pygame.sprite.Group()
    pociski = pygame.sprite.Group()

    # Tworzenie gracza
    gracz = Gracz(100, 400)
    all_sprites.add(gracz)

    # Tworzenie przeciwników
    for i in range(3):
        przeciwnik = Przeciwnik(300 + i * 150, 450)
        all_sprites.add(przeciwnik)
        przeciwnicy.add(przeciwnik)

    # Tło - jeśli plik nie istnieje, tworzymy zastępcze tło
    try:
        tlo = load_image("background.png")
        tlo = pygame.transform.scale(tlo, (SZEROKOSC, WYSOKOSC))
    except:
        tlo = pygame.Surface((SZEROKOSC, WYSOKOSC))
        tlo.fill((100, 100, 200))  # Niebieskie tło jeśli brak pliku

    running = True
    while running:
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Strzał
                    pocisk = Pocisk(gracz.rect.centerx, gracz.rect.centery, gracz.kierunek)
                    all_sprites.add(pocisk)
                    pociski.add(pocisk)

        # Aktualizacja
        all_sprites.update()

        # Kolizje: Pocisk z przeciwnikiem
        for pocisk in pociski:
            trafienia = pygame.sprite.spritecollide(pocisk, przeciwnicy, True)
            for przeciwnik in trafienia:
                pocisk.kill()

        # Rysowanie
        ekran.blit(tlo, (0, 0))
        all_sprites.draw(ekran)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
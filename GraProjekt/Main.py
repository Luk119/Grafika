import pygame
import sys

# Inicjalizacja PyGame
pygame.init()

# Ustawienia ekranu
SZEROKOSC = 1824
WYSOKOSC = 1200
WYSOKOSC_PODLOGI = 1000
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Szczurołap 007")

# Kolory
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)


# Ładowanie grafik
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


# Klasa Gracza
class Gracz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animacje = {
            "idle": [load_image("playerIdle.png")],
            "run": [
                load_image("playerRun1.png"),
                load_image("playerRun2.png")
            ],
            "jump_up": [load_image("playerJumpUp.png")],
            "jump_down": [load_image("playerJumpDown.png")],
            "land": [load_image("playerLand.png")],
        }
        self.obecna_animacja = "idle"
        self.klatka_animacji = 0
        self.czas_animacji = 0
        self.image = self.animacje[self.obecna_animacja][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y  # Używamy bottom zamiast y, aby lepiej kontrolować pozycję względem podłogi
        self.predkosc = 5
        self.skok = False
        self.sila_skoku = 30
        self.grawitacja = 0.6
        self.vel_y = 0
        self.kierunek = 1
        self.czy_laduje = False
        self.czas_ladowania = 0
        self.max_czas_ladowania = 0.4 * 60

    def update_animacja(self):
        if self.obecna_animacja == "run":
            self.czas_animacji += 1
            if self.czas_animacji >= 10:
                self.czas_animacji = 0
                self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje["run"])
                self.image = self.animacje["run"][self.klatka_animacji]
                if self.kierunek == -1:
                    self.image = pygame.transform.flip(self.image, True, False)

    def update(self, przeciwnicy):
        keys = pygame.key.get_pressed()

        if not self.czy_laduje:
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
                self.image = self.animacje["idle"][0]

        if keys[pygame.K_SPACE] and not self.skok and not self.czy_laduje:
            self.vel_y = -self.sila_skoku
            self.skok = True
            self.obecna_animacja = "jump_up"
            self.image = self.animacje["jump_up"][0]

        if self.skok:
            if self.vel_y < 0:
                self.obecna_animacja = "jump_up"
            else:
                self.obecna_animacja = "jump_down"

            self.image = self.animacje[self.obecna_animacja][0]

            # Obracamy tylko wtedy, gdy rzeczywiście zmienia się animacja skoku
            if self.kierunek == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        self.vel_y += self.grawitacja
        self.rect.y += self.vel_y

        # Sprawdzamy kolizję z przeciwnikami podczas spadania
        if self.vel_y > 0:  # Tylko gdy spadamy
            for przeciwnik in przeciwnicy:
                if (self.rect.bottom >= przeciwnik.rect.top and
                        self.rect.bottom <= przeciwnik.rect.top + 20 and  # Tolerancja 20 pikseli
                        self.rect.left < przeciwnik.rect.right and
                        self.rect.right > przeciwnik.rect.left):
                    # Zabijamy przeciwnika
                    przeciwnicy.remove(przeciwnik)
                    przeciwnik.kill()

                    # Odbijamy się lekko po zabiciu przeciwnika
                    self.vel_y = -self.sila_skoku / 2
                    break
            else:  # Jeśli nie trafiliśmy na przeciwnika
                if self.rect.bottom >= WYSOKOSC_PODLOGI:
                    self.rect.bottom = WYSOKOSC_PODLOGI
                    self.vel_y = 0
                    if self.skok:
                        self.obecna_animacja = "land"
                        self.image = self.animacje["land"][0]

                        # Obracanie postaci przy lądowaniu
                        if self.kierunek == -1:
                            self.image = pygame.transform.flip(self.image, True, False)

                        self.czy_laduje = True
                        self.czas_ladowania = self.max_czas_ladowania
                        self.skok = False
        else:  # Jeśli nie spadamy
            if self.rect.bottom >= WYSOKOSC_PODLOGI:
                self.rect.bottom = WYSOKOSC_PODLOGI
                self.vel_y = 0
                if self.skok:
                    self.obecna_animacja = "land"
                    self.image = self.animacje["land"][0]

                    # Obracanie postaci przy lądowaniu
                    if self.kierunek == -1:
                        self.image = pygame.transform.flip(self.image, True, False)

                    self.czy_laduje = True
                    self.czas_ladowania = self.max_czas_ladowania
                    self.skok = False

        if self.czy_laduje:
            self.czas_ladowania -= 1
            if self.czas_ladowania <= 0:
                self.czy_laduje = False
                self.obecna_animacja = "idle"
                self.image = self.animacje["idle"][0]

        self.update_animacja()


# Klasa Przeciwnika
class Przeciwnik(pygame.sprite.Sprite):
    def __init__(self, x, wysokosc_podlogi):
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
        # Ustawiamy przeciwników na podłodze (bottom = WYSOKOSC_PODLOGI)
        self.rect.bottom = wysokosc_podlogi
        self.predkosc = 2
        self.kierunek = 1

    def update(self):
        self.rect.x += self.predkosc * self.kierunek

        # Odbicie od ścian
        if self.rect.x <= 0 or self.rect.x >= SZEROKOSC - self.rect.width:
            self.kierunek *= -1  # Zmiana kierunku
            self.image = pygame.transform.flip(self.image, True, False)  # Obrót przeciwnika

        # Animacja
        self.czas_animacji += 1
        if self.czas_animacji >= 15:
            self.czas_animacji = 0
            self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje)
            self.image = self.animacje[self.klatka_animacji]

            # Obracanie przeciwnika zgodnie z kierunkiem ruchu
            if self.kierunek == 1:
                self.image = pygame.transform.flip(self.image, True, False)


def main():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    przeciwnicy = pygame.sprite.Group()

    # Tworzymy gracza - ustawiamy go na podłodze (bottom=WYSOKOSC_PODLOGI)
    gracz = Gracz(100, WYSOKOSC_PODLOGI)
    all_sprites.add(gracz)

    # Tworzymy przeciwników na podłodze
    for i in range(3):
        przeciwnik = Przeciwnik(300 + i * 150, WYSOKOSC_PODLOGI)
        all_sprites.add(przeciwnik)
        przeciwnicy.add(przeciwnik)

    # Ładowanie tła
    try:
        tlo = pygame.image.load("background2.png").convert()
        tlo = pygame.transform.scale(tlo, (SZEROKOSC, WYSOKOSC))
    except pygame.error as e:
        print(f"Nie można załadować tła: {e}")
        tlo = pygame.Surface((SZEROKOSC, WYSOKOSC))
        tlo.fill((100, 100, 200))

    try:
        podloga = pygame.image.load("ground.png").convert_alpha()
        podloga = pygame.transform.scale(podloga, (SZEROKOSC, WYSOKOSC - WYSOKOSC_PODLOGI))
    except pygame.error as e:
        print(f"Nie można załadować podłogi: {e}")
        podloga = pygame.Surface((SZEROKOSC, WYSOKOSC - WYSOKOSC_PODLOGI))
        podloga.fill((100, 70, 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gracz.update(przeciwnicy)
        przeciwnicy.update()

        ekran.blit(tlo, (0, 0))
        ekran.blit(podloga, (0, WYSOKOSC_PODLOGI))
        all_sprites.draw(ekran)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
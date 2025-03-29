import pygame
import sys

# Inicjalizacja PyGame
pygame.init()

# Ustawienia ekranu
SZEROKOSC = 1824
WYSOKOSC = 1200
WYSOKOSC_PODLOGI = 900
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
    except pygame.error as e:
        print(f"Błąd ładowania obrazu: {path}")
        print(f"Błąd: {e}")
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
            "run": [
                load_image("playerRun1.png"),  # Pierwsza klatka biegu
                load_image("playerJumpDown.png")  # Druga klatka biegu
            ],
            "jump_up": [load_image("playerJumpDown.png")],
            "jump_down": [load_image("playerJumpDown.png")],
            "land": [load_image("playerLand.png")],
            "attack": [load_image("playerIdle.png")],
        }
        self.obecna_animacja = "idle"
        self.image = self.animacje[self.obecna_animacja][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.predkosc = 5
        self.skok = False
        self.sila_skoku = 20
        self.grawitacja = 0.6
        self.vel_y = 0
        self.kierunek = 1
        self.czy_laduje = False
        self.czas_ladowania = 0
        self.max_czas_ladowania = 12
        self.poprzednia_animacja = "idle"

        # Animacja biegu
        self.klatka_biegu = 0
        self.czas_animacji = 0
        self.czas_zmiany_klatki = 10  # Co 10 klatek zmiana (przy 60 FPS to ~6 klatek/sekundę)

    def update(self):
        keys = pygame.key.get_pressed()

        # Zapamiętanie poprzedniej animacji
        self.poprzednia_animacja = self.obecna_animacja

        # Sterowanie tylko gdy nie lądujemy
        if not self.czy_laduje:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.predkosc
                self.kierunek = -1
                if not self.skok:
                    self.obecna_animacja = "run"
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.predkosc
                self.kierunek = 1
                if not self.skok:
                    self.obecna_animacja = "run"
            elif not self.skok:
                self.obecna_animacja = "idle"
                self.klatka_biegu = 0  # Reset animacji biegu gdy stoimy

        # Aktualizacja animacji biegu
        if self.obecna_animacja == "run" and not self.skok and not self.czy_laduje:
            self.czas_animacji += 1
            if self.czas_animacji >= self.czas_zmiany_klatki:
                self.czas_animacji = 0
                self.klatka_biegu = (self.klatka_biegu + 1) % len(self.animacje["run"])

        # Skok
        if keys[pygame.K_SPACE] and not self.skok and not self.czy_laduje:
            self.vel_y = -self.sila_skoku
            self.skok = True
            self.obecna_animacja = "jump_up"

        # Zmiana animacji w trakcie skoku
        if self.skok:
            if self.vel_y < 0:
                self.obecna_animacja = "jump_up"
            else:
                self.obecna_animacja = "jump_down"

        # Grawitacja
        self.vel_y += self.grawitacja
        self.rect.y += self.vel_y

        # Kolizja z podłożem
        if self.rect.y >= WYSOKOSC_PODLOGI:
            self.rect.y = WYSOKOSC_PODLOGI
            self.vel_y = 0

            if self.skok or self.poprzednia_animacja in ["jump_up", "jump_down"]:
                self.obecna_animacja = "land"
                self.czy_laduje = True
                self.czas_ladowania = self.max_czas_ladowania
                self.skok = False
            elif not self.czy_laduje:
                self.obecna_animacja = "idle"

        # Animacja lądowania
        if self.czy_laduje:
            self.czas_ladowania -= 1
            if self.czas_ladowania <= 0:
                self.czy_laduje = False
                self.obecna_animacja = "idle"

        # Atak
        if not self.skok and not self.czy_laduje:
            if keys[pygame.K_z]:
                self.obecna_animacja = "attack"

        # Aktualizacja obrazu
        if self.obecna_animacja == "run":
            self.image = self.animacje["run"][self.klatka_biegu]
        else:
            self.image = self.animacje[self.obecna_animacja][0]

        if self.kierunek == -1:
            self.image = pygame.transform.flip(self.image, True, False)
# Klasa Przeciwnika
class Przeciwnik(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("playerIdle.png")
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


# Główna pętla gry
def main():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    przeciwnicy = pygame.sprite.Group()

    # Tworzenie gracza
    gracz = Gracz(100, WYSOKOSC_PODLOGI - 200)
    all_sprites.add(gracz)

    # Tworzenie przeciwników
    for i in range(3):
        przeciwnik = Przeciwnik(300 + i * 150, WYSOKOSC_PODLOGI - 100)
        all_sprites.add(przeciwnik)
        przeciwnicy.add(przeciwnik)

    # Ładowanie tła
    try:
        tlo = pygame.image.load("background.png").convert()
        tlo = pygame.transform.scale(tlo, (SZEROKOSC, WYSOKOSC))
    except pygame.error as e:
        print(f"Nie można załadować tła: {e}")
        tlo = pygame.Surface((SZEROKOSC, WYSOKOSC))
        tlo.fill((100, 100, 200))  # Niebieskie tło jeśli brak pliku

    podloga = pygame.Surface((SZEROKOSC, WYSOKOSC - WYSOKOSC_PODLOGI))
    podloga.fill((100, 70, 30))  # Brązowy kolor podłogi

    running = True
    while running:
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aktualizacja
        all_sprites.update()

        # Rysowanie
        ekran.blit(tlo, (0, 0))
        ekran.blit(podloga, (0, WYSOKOSC_PODLOGI))  # Rysuj podłogę
        all_sprites.draw(ekran)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
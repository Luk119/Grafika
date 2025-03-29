import pygame
import sys

# Inicjalizacja PyGame
pygame.init()

# Ustawienia ekranu
SZEROKOSC = 1824
WYSOKOSC = 1200
WYSOKOSC_PODLOGI = 900
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Prosta RPG z pełnymi animacjami")

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
        # Zastępcza grafika z kolorem i napisem
        surf = pygame.Surface((50, 80), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0, 128), (0, 0, 50, 80))
        font = pygame.font.SysFont(None, 20)
        text = font.render(path.split('.')[0], True, BIALY)
        surf.blit(text, (5, 30))
        return surf

# Klasa Gracza
class Gracz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Ładowanie wszystkich animacji
        self.animacje = {
            "idle": [load_image("playerIdle.png")],
            "run": [
                load_image("playerRun2.png"),  # Lewa noga z przodu
                load_image("playerIdle.png")   # Prawa noga z przodu
            ],
            "jump_up": [load_image("playerIdle.png")],    # Animacja wznoszenia
            "jump_down": [load_image("playerJumpDown1.png")], # Animacja opadania
            "land": [load_image("playerLand.png")],
            "attack": [load_image("playerIdle.png")],
        }

        # Parametry animacji
        self.obecna_animacja = "idle"
        self.klatka_animacji = 0
        self.czas_animacji = 0
        self.szybkosc_animacji = 0.15  # Im mniejsza wartość, tym szybsza animacja

        self.image = self.animacje[self.obecna_animacja][self.klatka_animacji]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Fizyka
        self.predkosc = 5
        self.skok = False
        self.sila_skoku = 20
        self.grawitacja = 0.6
        self.vel_y = 0
        self.kierunek = 1  # 1 dla prawo, -1 dla lewo

        # Stan lądowania
        self.czy_laduje = False
        self.czas_ladowania = 0
        self.max_czas_ladowania = 0.4 * 60  # 0.2 sekundy

    def update_animacja(self):
        # Aktualizacja klatek animacji
        if self.obecna_animacja in ["run", "attack"]:
            self.czas_animacji += 1
            if self.czas_animacji >= self.szybkosc_animacji * 60:
                self.czas_animacji = 0
                self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje[self.obecna_animacja])

        # Ustawienie odpowiedniej klatki animacji
        self.image = self.animacje[self.obecna_animacja][self.klatka_animacji]
        if self.kierunek == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        keys = pygame.key.get_pressed()

        # Reset animacji jeśli zmieniamy stan (ale nie podczas skoku/lądowania)
        if self.obecna_animacja not in ["jump_up", "jump_down", "land"]:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                if self.obecna_animacja != "run":
                    self.obecna_animacja = "run"
                    self.klatka_animacji = 0
                    self.czas_animacji = 0
            else:
                if self.obecna_animacja != "idle":
                    self.obecna_animacja = "idle"
                    self.klatka_animacji = 0

        # Poruszanie się
        if not self.czy_laduje:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.predkosc
                self.kierunek = -1
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.predkosc
                self.kierunek = 1

        # Skok
        if keys[pygame.K_SPACE] and not self.skok and not self.czy_laduje:
            self.vel_y = -self.sila_skoku
            self.skok = True
            self.obecna_animacja = "jump_up"
            self.klatka_animacji = 0

        # Zmiana animacji w trakcie skoku
        if self.skok:
            if self.vel_y < 0:  # Wznoszenie
                self.obecna_animacja = "jump_up"
            else:  # Opadanie
                self.obecna_animacja = "jump_down"

        # Grawitacja
        self.vel_y += self.grawitacja
        self.rect.y += self.vel_y

        # Kolizja z podłożem
        if self.rect.y >= WYSOKOSC_PODLOGI:
            self.rect.y = WYSOKOSC_PODLOGI
            self.vel_y = 0

            if self.skok or self.obecna_animacja in ["jump_up", "jump_down"]:
                self.obecna_animacja = "land"
                self.czy_laduje = True
                self.czas_ladowania = self.max_czas_ladowania
                self.skok = False
                self.klatka_animacji = 0

        # Lądowanie
        if self.czy_laduje:
            self.czas_ladowania -= 1
            if self.czas_ladowania <= 0:
                self.czy_laduje = False
                self.obecna_animacja = "idle"
                self.klatka_animacji = 0

        # Atak
        if keys[pygame.K_z] and not self.skok and not self.czy_laduje:
            self.obecna_animacja = "attack"
            self.klatka_animacji = 0

        # Aktualizacja animacji
        self.update_animacja()

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
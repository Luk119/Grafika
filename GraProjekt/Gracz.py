from Stale import *
from LoadImage import *
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
        self.rect.bottom = y
        self.predkosc = 5
        self.skok = False
        self.sila_skoku = 27
        self.grawitacja = 0.9
        self.vel_y = 0
        self.kierunek = 1
        self.czy_laduje = False
        self.czas_ladowania = 0
        self.max_czas_ladowania = 0.4 * 60
        self.zycie = 5  # Dodajemy życie gracza (5 punktów)
        self.obrazenia = False  # Flaga obrażeń
        self.czas_obrazen = 0  # Czas odporności po otrzymaniu obrażeń
        self.max_czas_obrazen = 1 * 60  # 1 sekunda odporności

    def update_animacja(self):
        if self.obecna_animacja == "run":
            self.czas_animacji += 1
            if self.czas_animacji >= 10:
                self.czas_animacji = 0
                self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje["run"])
                self.image = self.animacje["run"][self.klatka_animacji]
                if self.kierunek == -1:
                    self.image = pygame.transform.flip(self.image, True, False)

    def update(self, przeciwnicy, stan_gry):
        keys = pygame.key.get_pressed()

        # Obsługa odporności po obrażeniach
        if self.obrazenia:
            self.czas_obrazen -= 1
            if self.czas_obrazen <= 0:
                self.obrazenia = False

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

            if self.kierunek == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        self.vel_y += self.grawitacja
        self.rect.y += self.vel_y

        if self.vel_y > 0:  # Tylko gdy spadamy
            for przeciwnik in przeciwnicy:
                if (self.rect.bottom >= przeciwnik.rect.top and
                        self.rect.bottom <= przeciwnik.rect.top + 20 and
                        self.rect.left < przeciwnik.rect.right and
                        self.rect.right > przeciwnik.rect.left):
                    # Zabijamy przeciwnika i dodajemy punkty
                    przeciwnicy.remove(przeciwnik)
                    przeciwnik.kill()
                    stan_gry.punkty += 100  # Dodaj 100 punktów za każdego przeciwnika

                    self.vel_y = -self.sila_skoku / 2
                    break
            else:
                if self.rect.bottom >= WYSOKOSC_PODLOGI:
                    self.rect.bottom = WYSOKOSC_PODLOGI
                    self.vel_y = 0
                    if self.skok:
                        self.obecna_animacja = "land"
                        self.image = self.animacje["land"][0]

                        if self.kierunek == -1:
                            self.image = pygame.transform.flip(self.image, True, False)

                        self.czy_laduje = True
                        self.czas_ladowania = self.max_czas_ladowania
                        self.skok = False
        else:
            if self.rect.bottom >= WYSOKOSC_PODLOGI:
                self.rect.bottom = WYSOKOSC_PODLOGI
                self.vel_y = 0
                if self.skok:
                    self.obecna_animacja = "land"
                    self.image = self.animacje["land"][0]

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

        for przeciwnik in przeciwnicy:
            if self.rect.colliderect(przeciwnik.rect) and not self.obrazenia:
                # Sprawdź czy kolizja jest od góry (skok na przeciwnika)
                if (self.vel_y > 0 and
                        self.rect.bottom >= przeciwnik.rect.top and
                        self.rect.bottom <= przeciwnik.rect.top + 20):

                    # Zabij przeciwnika (istniejący kod)
                    przeciwnicy.remove(przeciwnik)
                    przeciwnik.kill()
                    stan_gry.punkty += 100
                    self.vel_y = -self.sila_skoku / 2
                    break
                else:
                    # Kolizja boczna - otrzymaj obrażenia
                    self.zycie -= 1
                    self.obrazenia = True
                    self.czas_obrazen = self.max_czas_obrazen

                    # Odbij gracza w przeciwnym kierunku
                    if self.rect.centerx < przeciwnik.rect.centerx:
                        self.rect.x -= 50  # Odbij w lewo
                    else:
                        self.rect.x += 50  # Odbij w prawo

                    # Sprawdź czy gracz stracił wszystkie życia
                    if self.zycie <= 0:
                        stan_gry.czy_koniec_gry = True
                    break

        self.update_animacja()
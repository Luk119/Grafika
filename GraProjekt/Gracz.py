# Klasa Gracza
from Stale import *  # importuje stałe gry, np. szerokość/ wysokość ekranu, podłogi itp.
from LoadImage import *  # importuje funkcję do ładowania i skalowania obrazów


class Gracz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # inicjalizacja klasy bazowej Sprite

        # Słownik animacji gracza — każda akcja (bezczynność, bieg, skok) zawiera listę klatek
        self.animacje = {
            "idle": [load_image("gameImages/playerIdle.png")],  # animacja stania w miejscu
            "run": [
                load_image("gameImages/playerRun1.png"),
                load_image("gameImages/playerRun2.png")
            ],
            "jump_up": [load_image("gameImages/playerJumpUp.png")],  # animacja skoku w górę
            "jump_down": [load_image("gameImages/playerJumpDown.png")],  # animacja spadania
            "land": [load_image("gameImages/playerLand.png")],  # animacja lądowania
        }

        self.obecna_animacja = "idle"  # początkowy stan animacji
        self.klatka_animacji = 0  # indeks aktualnej klatki
        self.czas_animacji = 0  # licznik czasu do zmiany klatki
        self.image = self.animacje["idle"][0]  # aktualny obrazek gracza
        self.rect = self.image.get_rect()  # prostokąt kolizji
        self.rect.x = x  # pozycja gracza w poziomie
        self.rect.bottom = y  # dolna krawędź — gracz stoi na podłodze

        # Ruch i fizyka
        self.predkosc = 5  # prędkość poruszania się w poziomie
        self.skok = False  # czy gracz aktualnie skacze
        self.sila_skoku = 27  # siła skoku
        self.grawitacja = 0.8  # wartość grawitacji
        self.vel_y = 0  # prędkość w osi Y (pion)

        self.kierunek = 1  # 1 = prawo, -1 = lewo

        # Lądowanie po skoku
        self.czy_laduje = False  # czy aktualnie trwa animacja lądowania
        self.czas_ladowania = 0  # licznik lądowania
        self.max_czas_ladowania = 0.25 * 60  # maksymalny czas lądowania (0.25 sekundy)

        # Życie i obrażenia
        self.zycie = 5  # liczba żyć
        self.obrazenia = False  # flaga, czy gracz został trafiony
        self.czas_obrazen = 0  # licznik nieśmiertelności
        self.max_czas_obrazen = 1 * 60  # nieśmiertelność trwa 1 sekundę

    # Funkcja odpowiedzialna za zmianę animacji biegu
    def update_animacja(self):
        if self.obecna_animacja == "run":
            self.czas_animacji += 1
            if self.czas_animacji >= 10:  # zmiana co 10 klatek
                self.czas_animacji = 0
                self.klatka_animacji = (self.klatka_animacji + 1) % len(self.animacje["run"])
                self.image = self.animacje["run"][self.klatka_animacji]
                if self.kierunek == -1:  # jeśli lewo, odbij obraz
                    self.image = pygame.transform.flip(self.image, True, False)

    # Główna funkcja update
    def update(self, przeciwnicy, stan_gry):
        keys = pygame.key.get_pressed()

        # Obsługa nieśmiertelności po otrzymaniu obrażeń
        if self.obrazenia:
            self.czas_obrazen -= 1
            if self.czas_obrazen <= 0:
                self.obrazenia = False

        # Poruszanie się w poziomie
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

        # Skok
        if keys[pygame.K_UP] and not self.skok and not self.czy_laduje:
            self.vel_y = -self.sila_skoku
            self.skok = True
            self.obecna_animacja = "jump_up"
            self.image = self.animacje["jump_up"][0]

        # W czasie skoku
        if self.skok:
            if self.vel_y < 0:
                self.obecna_animacja = "jump_up"
            else:
                self.obecna_animacja = "jump_down"
            self.image = self.animacje[self.obecna_animacja][0]
            if self.kierunek == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        # Grawitacja
        self.vel_y += self.grawitacja
        self.rect.y += self.vel_y

        # Spadanie — sprawdzanie kolizji z przeciwnikiem od góry
        if self.vel_y > 0:
            for przeciwnik in przeciwnicy:
                if (self.rect.bottom >= przeciwnik.rect.top and
                        self.rect.bottom <= przeciwnik.rect.top + 20 and
                        self.rect.left < przeciwnik.rect.right and
                        self.rect.right > przeciwnik.rect.left):
                    przeciwnicy.remove(przeciwnik)
                    przeciwnik.kill()
                    stan_gry.punkty += 100
                    self.vel_y = -self.sila_skoku / 2
                    break
            else:
                # Lądowanie na ziemi
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

        # Licznik animacji lądowania
        if self.czy_laduje:
            self.czas_ladowania -= 1
            if self.czas_ladowania <= 0:
                self.czy_laduje = False
                self.obecna_animacja = "idle"
                self.image = self.animacje["idle"][0]

        # Kolizja boczna z przeciwnikiem
        for przeciwnik in przeciwnicy:
            if self.rect.colliderect(przeciwnik.rect) and not self.obrazenia:
                if (self.vel_y > 0 and
                        self.rect.bottom >= przeciwnik.rect.top and
                        self.rect.bottom <= przeciwnik.rect.top + 20):

                    przeciwnicy.remove(przeciwnik)
                    przeciwnik.kill()
                    stan_gry.punkty += 100
                    self.vel_y = -self.sila_skoku / 2
                    break
                else:
                    self.zycie -= 1
                    self.obrazenia = True
                    self.czas_obrazen = self.max_czas_obrazen

                    # Odbicie gracza w przeciwnym kierunku
                    if self.rect.centerx < przeciwnik.rect.centerx:
                        self.rect.x -= 50
                        self.rect.y -= 30
                    else:
                        self.rect.x += 50
                        self.rect.y -= 30

                    if self.zycie <= 0:
                        stan_gry.czy_koniec_gry = True
                    break

        # Na koniec — aktualizacja animacji biegu
        self.update_animacja()

import sys
from Przeciwnik import *
from Gracz import *
from Stale import *

# Stan gry
class StanGry:
    def __init__(self):
        self.punkty = 0
        self.poziom = 1
        self.max_poziom = 5
        self.czy_wyswietlac_komunikat = False
        self.czas_komunikatu = 0
        self.max_czas_komunikatu = 2 * 60
        self.czy_wygrana = False
        self.czy_koniec_gry = False

def nowy_poziom(stan_gry, all_sprites, przeciwnicy, gracz):
    # Usuń wszystkich przeciwników
    for przeciwnik in przeciwnicy:
        przeciwnik.kill()
    przeciwnicy.empty()

    # Utwórz nowych przeciwników (liczba równa poziomowi + 2)
    liczba_przeciwnikow = stan_gry.poziom + 2
    predkosc_przeciwnikow = 2 + stan_gry.poziom * 2.3 # Zwiększ prędkość z każdym poziomem

    for i in range(liczba_przeciwnikow):
        x = 300 + i * (SZEROKOSC - 600) // liczba_przeciwnikow
        przeciwnik = Przeciwnik(x, WYSOKOSC_PODLOGI, predkosc_przeciwnikow)
        all_sprites.add(przeciwnik)
        przeciwnicy.add(przeciwnik)

    # Ustaw gracza na początku poziomu
    gracz.rect.x = 100
    gracz.rect.bottom = WYSOKOSC_PODLOGI
    gracz.vel_y = 0
    gracz.skok = False
    gracz.czy_laduje = False
    gracz.obecna_animacja = "idle"
    gracz.image = gracz.animacje["idle"][0]

    # Wyświetl komunikat o nowym poziomie
    stan_gry.czy_wyswietlac_komunikat = True
    stan_gry.czas_komunikatu = stan_gry.max_czas_komunikatu


def main():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    przeciwnicy = pygame.sprite.Group()
    stan_gry = StanGry()

    gracz = Gracz(100, WYSOKOSC_PODLOGI)
    all_sprites.add(gracz)

    # Rozpocznij pierwszy poziom
    nowy_poziom(stan_gry, all_sprites, przeciwnicy, gracz)

    try:
        tlo = pygame.image.load("gameImages/background.png").convert()
        tlo = pygame.transform.scale(tlo, (SZEROKOSC, WYSOKOSC))
    except pygame.error as e:
        print(f"Nie można załadować tła: {e}")
        tlo = pygame.Surface((SZEROKOSC, WYSOKOSC))
        tlo.fill((100, 100, 200))

    try:
        podloga = pygame.image.load("gameImages/ground.png").convert_alpha()
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

        gracz.update(przeciwnicy, stan_gry)
        przeciwnicy.update()

        # Sprawdź czy wszyscy przeciwnicy zostali pokonani
        if len(przeciwnicy) == 0 and not stan_gry.czy_wyswietlac_komunikat:
            if stan_gry.poziom < stan_gry.max_poziom:
                stan_gry.poziom += 1
                nowy_poziom(stan_gry, all_sprites, przeciwnicy, gracz)
            else:
                stan_gry.czy_wygrana = True
                stan_gry.czy_wyswietlac_komunikat = True
                stan_gry.czas_komunikatu = stan_gry.max_czas_komunikatu

        # Aktualizuj czas wyświetlania komunikatu
        if stan_gry.czy_wyswietlac_komunikat:
            stan_gry.czas_komunikatu -= 1
            if stan_gry.czas_komunikatu <= 0:
                stan_gry.czy_wyswietlac_komunikat = False

        ekran.blit(tlo, (0, 0))
        ekran.blit(podloga, (0, WYSOKOSC_PODLOGI))
        all_sprites.draw(ekran)

        # Wyświetlanie punktów i poziomu
        tekst_punkty = czcionka.render(f"Punkty: {stan_gry.punkty}", True, BIALY)
        ekran.blit(tekst_punkty, (20, WYSOKOSC - 50))

        tekst_poziom = czcionka.render(f"Poziom: {stan_gry.poziom}/{stan_gry.max_poziom}", True, BIALY)
        ekran.blit(tekst_poziom, (20, WYSOKOSC - 100))

        # Wyświetlanie komunikatu o nowym poziomie lub wygranej
        if stan_gry.czy_wyswietlac_komunikat:
            if stan_gry.czy_wygrana:
                tekst_komunikat = duza_czcionka.render("Zwycięstwo!", True, ZIELONY)
            else:
                tekst_komunikat = duza_czcionka.render(f"Poziom {stan_gry.poziom}", True, ZIELONY)

            szerokosc_tekstu = tekst_komunikat.get_width()
            ekran.blit(tekst_komunikat, (SZEROKOSC // 2 - szerokosc_tekstu // 2, WYSOKOSC // 2 - 100))

        # Wyświetlanie życia
        tekst_zycie = czcionka.render(f"Zdrowie: {' 0' * gracz.zycie}", True, CZARNY)
        ekran.blit(tekst_zycie, (20, WYSOKOSC - 150))
        tekst_zycie = czcionka.render(f"Zdrowie: {' 0' * gracz.zycie}", True, ZIELONY)
        ekran.blit(tekst_zycie, (22, WYSOKOSC - 152))

        # Sprawdź koniec gry
        if stan_gry.czy_koniec_gry:
            tekst_koniec = duza_czcionka.render("Porażka!", True, CZERWONY)
            szerokosc_tekstu = tekst_koniec.get_width()
            ekran.blit(tekst_koniec, (SZEROKOSC // 2 - szerokosc_tekstu // 2, WYSOKOSC // 2 - 100))
            pygame.display.flip()
            pygame.time.wait(3000)  # Czekaj 3 sekundy
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
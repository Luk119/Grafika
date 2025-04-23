import sys
from Przeciwnik import *
from Gracz import *
from Stale import *

# stan gry
class StanGry:
    def __init__(self):  # konstruktor inicjalizujący stan gry
        self.punkty = 0  # liczba punktów zdobytych przez gracza
        self.poziom = 1  # aktualny poziom gry
        self.max_poziom = 5  # maksymalny poziom gry
        self.czy_wyswietlac_komunikat = False  # czy wyświetlać komunikat (np. nowy poziom)
        self.czas_komunikatu = 0  # czas wyświetlania komunikatu
        self.max_czas_komunikatu = 2 * 60  # maksymalny czas komunikatu (w klatkach)
        self.czy_wygrana = False  # czy gracz wygrał
        self.czy_koniec_gry = False  # czy gra się zakończyła

def nowy_poziom(stan_gry, all_sprites, przeciwnicy, gracz):
    # usuń wszystkich przeciwników
    for przeciwnik in przeciwnicy:
        przeciwnik.kill()  # usuń przeciwnika ze wszystkich grup
    przeciwnicy.empty()  # wyczyść grupę przeciwników

    # utwórz nowych przeciwników (liczba równa poziomowi + 2)
    liczba_przeciwnikow = stan_gry.poziom + 2  # liczba przeciwników zależna od poziomu
    predkosc_przeciwnikow = 2 + stan_gry.poziom * 1.4  # zwiększ prędkość wraz z poziomem

    for i in range(liczba_przeciwnikow):  # twórz kolejnych przeciwników
        x = 300 + i * (SZEROKOSC - 300) // liczba_przeciwnikow  # oblicz pozycję X
        przeciwnik = Przeciwnik(x, WYSOKOSC_PODLOGI, predkosc_przeciwnikow)  # utwórz przeciwnika
        all_sprites.add(przeciwnik)  # dodaj do grupy wszystkich sprite’ów
        przeciwnicy.add(przeciwnik)  # dodaj do grupy przeciwników

    # ustaw gracza na początku poziomu
    gracz.rect.x = 100  # pozycja X gracza
    gracz.rect.bottom = WYSOKOSC_PODLOGI  # ustaw dolną krawędź gracza na poziomie podłogi
    gracz.vel_y = 0  # zresetuj prędkość pionową
    gracz.skok = False  # zresetuj flagę skoku
    gracz.czy_laduje = False  # zresetuj flagę lądowania
    gracz.obecna_animacja = "idle"  # ustaw animację na bezczynność
    gracz.image = gracz.animacje["idle"][0]  # ustaw obraz gracza na pierwszy z animacji „idle”

    # wyświetl komunikat o nowym poziomie
    stan_gry.czy_wyswietlac_komunikat = True  # aktywuj wyświetlanie komunikatu
    stan_gry.czas_komunikatu = stan_gry.max_czas_komunikatu  # ustaw licznik czasu komunikatu

def main():
    clock = pygame.time.Clock()  # zegar do kontrolowania FPS
    all_sprites = pygame.sprite.Group()  # grupa wszystkich sprite’ów
    przeciwnicy = pygame.sprite.Group()  # grupa przeciwników
    stan_gry = StanGry()  # utwórz nowy stan gry

    gracz = Gracz(100, WYSOKOSC_PODLOGI)  # utwórz obiekt gracza
    all_sprites.add(gracz)  # dodaj gracza do grupy sprite’ów

    # rozpocznij pierwszy poziom
    nowy_poziom(stan_gry, all_sprites, przeciwnicy, gracz)

    try:
        tlo = pygame.image.load("gameImages/background.png").convert()  # wczytaj tło
        tlo = pygame.transform.scale(tlo, (SZEROKOSC, WYSOKOSC))  # przeskaluj tło
    except pygame.error as e:
        print(f"Nie można załadować tła: {e}")  # komunikat błędu
        tlo = pygame.Surface((SZEROKOSC, WYSOKOSC))  # utwórz powierzchnię zastępczą
        tlo.fill((100, 100, 200))  # nadaj jej kolor

    try:
        podloga = pygame.image.load("gameImages/ground.png").convert_alpha()  # wczytaj podłogę
        podloga = pygame.transform.scale(podloga, (SZEROKOSC, WYSOKOSC - WYSOKOSC_PODLOGI))  # przeskaluj ją
    except pygame.error as e:
        print(f"Nie można załadować podłogi: {e}")  # komunikat błędu
        podloga = pygame.Surface((SZEROKOSC, WYSOKOSC - WYSOKOSC_PODLOGI))  # utwórz powierzchnię zastępczą
        podloga.fill((100, 70, 30))  # nadaj jej kolor

    running = True  # flaga głównej pętli gry
    while running:
        for event in pygame.event.get():  # obsługa zdarzeń
            if event.type == pygame.QUIT:  # zamknięcie okna
                running = False  # zakończ grę

        gracz.update(przeciwnicy, stan_gry)  # zaktualizuj stan gracza
        przeciwnicy.update()  # zaktualizuj przeciwników

        # sprawdź czy wszyscy przeciwnicy zostali pokonani
        if len(przeciwnicy) == 0 and not stan_gry.czy_wyswietlac_komunikat:
            if stan_gry.poziom < stan_gry.max_poziom:
                stan_gry.poziom += 1  # przejdź do następnego poziomu
                nowy_poziom(stan_gry, all_sprites, przeciwnicy, gracz)  # zainicjuj nowy poziom
            else:
                stan_gry.czy_wygrana = True  # ustaw flagę wygranej
                stan_gry.czy_wyswietlac_komunikat = True  # pokaż komunikat
                stan_gry.czas_komunikatu = stan_gry.max_czas_komunikatu  # ustaw czas komunikatu

        # aktualizuj czas wyświetlania komunikatu
        if stan_gry.czy_wyswietlac_komunikat:
            stan_gry.czas_komunikatu -= 1  # zmniejsz licznik
            if stan_gry.czas_komunikatu <= 0:
                stan_gry.czy_wyswietlac_komunikat = False  # wyłącz komunikat

        ekran.blit(tlo, (0, 0))  # rysuj tło
        ekran.blit(podloga, (0, WYSOKOSC_PODLOGI))  # rysuj podłogę
        all_sprites.draw(ekran)  # narysuj wszystkie sprite’y

        # wyświetlanie punktów i poziomu
        tekst_punkty = czcionka.render(f"Punkty: {stan_gry.punkty}", True, BIALY)  # renderuj punkty
        ekran.blit(tekst_punkty, (20, WYSOKOSC - 50))  # wyświetl punkty

        tekst_poziom = czcionka.render(f"Poziom: {stan_gry.poziom}/{stan_gry.max_poziom}", True, BIALY)  # renderuj poziom
        ekran.blit(tekst_poziom, (20, WYSOKOSC - 100))  # wyświetl poziom

        # wyświetlanie komunikatu o nowym poziomie lub wygranej
        if stan_gry.czy_wyswietlac_komunikat:
            if stan_gry.czy_wygrana:
                tekst_komunikat = duza_czcionka.render("Zwycięstwo!", True, ZIELONY)  # komunikat o wygranej
            else:
                tekst_komunikat = duza_czcionka.render(f"Poziom {stan_gry.poziom}", True, ZIELONY)  # komunikat o nowym poziomie

            szerokosc_tekstu = tekst_komunikat.get_width()  # szerokość tekstu do wyśrodkowania
            ekran.blit(tekst_komunikat, (SZEROKOSC // 2 - szerokosc_tekstu // 2, WYSOKOSC // 2 - 100))  # wyśrodkuj komunikat

        # wyświetlanie życia
        tekst_zycie = czcionka.render(f"Zdrowie: {' 0' * gracz.zycie}", True, CZARNY)  # cień tekstu zdrowia
        ekran.blit(tekst_zycie, (20, WYSOKOSC - 150))  # rysuj cień
        tekst_zycie = czcionka.render(f"Zdrowie: {' 0' * gracz.zycie}", True, ZIELONY)  # zdrowie na zielono
        ekran.blit(tekst_zycie, (22, WYSOKOSC - 152))  # rysuj tekst lekko przesunięty

        # sprawdź koniec gry
        if stan_gry.czy_koniec_gry:
            tekst_koniec = duza_czcionka.render("Porażka!", True, CZERWONY)  # komunikat o porażce
            szerokosc_tekstu = tekst_koniec.get_width()  # szerokość tekstu do wyśrodkowania
            ekran.blit(tekst_koniec, (SZEROKOSC // 2 - szerokosc_tekstu // 2, WYSOKOSC // 2 - 100))  # wyśrodkuj tekst
            pygame.display.flip()  # odśwież ekran
            pygame.time.wait(3000)  # czekaj 3 sekundy
            running = False  # zakończ pętlę gry

        pygame.display.flip()  # odśwież ekran
        clock.tick(60)  # ogranicz FPS do 60

    pygame.quit()  # zakończ pygame
    sys.exit()  # zakończ program

if __name__ == "__main__":  # uruchom funkcję main tylko jeśli to główny plik
    main()

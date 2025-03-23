import pygame
import random

pygame.init()

# Inicjalizacja okna
win = pygame.display.set_mode((1000, 900))
pygame.display.set_caption("Pierwsza gra")

# Parametry obiektu
gx = 0
gy = 40
szerokosc = 20
wysokosc = 20
krok = 20

# Wczytanie obrazka gracza
gracz_image = pygame.image.load("gracz.jpg")  # Upewnij się, że masz obrazek w folderze gry
gracz_image = pygame.transform.scale(gracz_image, (szerokosc, wysokosc))  # Skalowanie do odpowiedniego rozmiaru

# Czcionka do wyświetlania tekstu
font = pygame.font.SysFont("Bradley Hand", 24)


# Funkcja do generowania nowych punktów
def generuj_punkty():
    punkty = []
    for _ in range(10):
        x_punkt = random.randint(0, 980)
        y_punkt = random.randint(0, 880)
        punkty.append(pygame.Rect(x_punkt, y_punkt, 20, 20))
    return punkty


# Funkcja do generowania nowych przeszkód
def generuj_przeszkody(przeszkody, przeszkody_prędkości):
    x_przeszkoda = random.randint(0, 980)
    y_przeszkoda = random.randint(0, 880)
    przeszkody.append(pygame.Rect(x_przeszkoda, y_przeszkoda, 20, 20))
    przeszkody_prędkości.append([random.choice([-7, 7]), random.choice([-7, 7])])  # Szybsze


# Inicjalizacja punktów i przeszkód
punkty = generuj_punkty()
czerwone_kwadraty = []
czerwone_prędkości = []
przeszkody = []
przeszkody_prędkości = []

# Generowanie 5 poruszających się czerwonych kwadratów
for _ in range(5):
    x_kwadrat = random.randint(0, 980)
    y_kwadrat = random.randint(0, 880)
    czerwone_kwadraty.append(pygame.Rect(x_kwadrat, y_kwadrat, 20, 20))
    czerwone_prędkości.append([random.choice([-5, 5]), random.choice([-5, 5])])

# Generowanie 5 poruszających się niebieskich kwadratów
for _ in range(5):
    x_przeszkoda = random.randint(0, 980)
    y_przeszkoda = random.randint(0, 880)
    przeszkody.append(pygame.Rect(x_przeszkoda, y_przeszkoda, 20, 20))
    przeszkody_prędkości.append([random.choice([-7, 7]), random.choice([-7, 7])])  # Szybsze

score = 0
run = True
while run:
    pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gx -= krok
    if keys[pygame.K_RIGHT]:
        gx += krok
    if keys[pygame.K_UP]:
        gy -= krok
    if keys[pygame.K_DOWN]:
        gy += krok

    # Przechodzenie przez krawędź
    if gx < 0:
        gx = 980  # Pojawienie się po prawej stronie
    elif gx > 980:
        gx = 0  # Pojawienie się po lewej stronie
    if gy < 0:
        gy = 880  # Pojawienie się na dole
    elif gy > 880:
        gy = 0  # Pojawienie się na górze

    zielony_kwadrat = pygame.Rect(gx, gy, szerokosc, wysokosc)

    win.fill((255, 197, 242))

    # Rysowanie i poruszanie czerwonych kwadratów
    for i, czerwony_kwadrat in enumerate(czerwone_kwadraty):
        czerwony_kwadrat.x += czerwone_prędkości[i][0]
        czerwony_kwadrat.y += czerwone_prędkości[i][1]

        # Odbijanie od ścian
        if czerwony_kwadrat.left <= 0 or czerwony_kwadrat.right >= 1000:
            czerwone_prędkości[i][0] *= -1
        if czerwony_kwadrat.top <= 0 or czerwony_kwadrat.bottom >= 900:
            czerwone_prędkości[i][1] *= -1

        pygame.draw.rect(win, (200, 30, 30), czerwony_kwadrat)

        # Sprawdzenie kolizji z czerwonym kwadratem
        if zielony_kwadrat.colliderect(czerwony_kwadrat):
            print("Przegrałeś!")
            run = False

    # Rysowanie i poruszanie niebieskich kwadratów
    for i, przeszkoda in enumerate(przeszkody):
        przeszkoda.x += przeszkody_prędkości[i][0]
        przeszkoda.y += przeszkody_prędkości[i][1]

        # Odbijanie od ścian
        if przeszkoda.left <= 0 or przeszkoda.right >= 1000:
            przeszkody_prędkości[i][0] *= -1
        if przeszkoda.top <= 0 or przeszkoda.bottom >= 900:
            przeszkody_prędkości[i][1] *= -1

        pygame.draw.rect(win, (0, 0, 255), przeszkoda)

        # Sprawdzenie kolizji z niebieskim kwadratem
        if zielony_kwadrat.colliderect(przeszkoda):
            print("Przegrałeś!")
            run = False

    # Rysowanie punktów do zbierania
    for punkt in punkty[:]:
        if zielony_kwadrat.colliderect(punkt):
            punkty.remove(punkt)
            score += 1
        pygame.draw.rect(win, (25, 125, 125), punkt)

    # Generowanie nowych punktów po zebraniu wszystkich
    if len(punkty) == 0:
        punkty = generuj_punkty()

    # Dodawanie nowej przeszkody co 10 punktów
    if score % 10 == 0 and len(przeszkody) < (score // 10 + 5):  # Dodanie nowej przeszkody
        generuj_przeszkody(przeszkody, przeszkody_prędkości)

    # Rysowanie obrazka gracza zamiast kwadratu
    win.blit(gracz_image, (gx, gy))  # Używamy obrazka w pozycji gracza

    # Wyświetlanie pozycji gracza
    if gx == 0 and gy == 0:
        position_text = font.render(f"x = {gx}, y = {gy}", True, (65, 105, 225))
        win.blit(position_text, (860, -2))
    elif (10 < gx < 100) and (10 < gy < 100):
        position_text = font.render(f"x = {gx}, y = {gy}", True, (65, 105, 225))
        win.blit(position_text, (830, -2))
    elif gx >= 100 and gy >= 100:
        position_text = font.render(f"x = {gx}, y = {gy}", True, (65, 105, 225))
        win.blit(position_text, (805, -2))
    elif gx >= 100 or gy >= 100:
        position_text = font.render(f"x = {gx}, y = {gy}", True, (65, 105, 225))
        win.blit(position_text, (817, -2))
    else:
        position_text = font.render(f"x = {gx}, y = {gy}", True, (65, 105, 225))
        win.blit(position_text, (845, -2))

    # Wyświetlanie wyniku
    score_text = font.render(f"score: {score}", True, (76, 187, 23))
    win.blit(score_text, (2, -2))

    pygame.display.update()

pygame.quit()

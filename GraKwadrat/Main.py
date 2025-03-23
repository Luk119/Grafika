import pygame
import random

pygame.init()

# Inicjalizacja okna
win = pygame.display.set_mode((1000, 900))
pygame.display.set_caption("Pierwsza gra")

# Parametry obiektu
x = 0
y = 40
szerokosc = 20
wysokosc = 20
krok = 20

# Czcionka do wyświetlania tekstu
font = pygame.font.SysFont("Bradley Hand", 24)

# Generowanie 10 losowych pozycji dla czerwonych kwadratów
czerwone_kwadraty = []
for _ in range(10):
    x_kwadrat = random.randint(0, 980)
    y_kwadrat = random.randint(0, 880)
    czerwone_kwadraty.append(pygame.Rect(x_kwadrat, y_kwadrat, 20, 20))


score = 0

run = True
while run:
    # Opóźnienie w grze
    pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= krok
    if keys[pygame.K_RIGHT]:
        x += krok
    if keys[pygame.K_UP]:
        y -= krok
    if keys[pygame.K_DOWN]:
        y += krok

    zielony_kwadrat = pygame.Rect(x, y, szerokosc, wysokosc)

    win.fill((225, 220, 150))

    # Rysowanie czerwonych kwadratów
    for czerwony_kwadrat in czerwone_kwadraty[:]:
        if zielony_kwadrat.colliderect(czerwony_kwadrat):
            czerwone_kwadraty.remove(czerwony_kwadrat)
            score += 1

        pygame.draw.rect(win, (200, 30, 30), czerwony_kwadrat)

    # Rysowanie pionka
    pygame.draw.rect(win, (25, 178, 22), zielony_kwadrat)

    #Wyświetlanie położenia zielonego kwadratu (tekst zmienia położenie w zależności od wartości x i y)
    if x == 0 and y == 0:
        position_text = font.render(f"x = {x}, y = {y}", True, (65, 105, 225))
        win.blit(position_text, (860, -2))
    elif (10 < x < 100) and (10 < y < 100):
        position_text = font.render(f"x = {x}, y = {y}", True, (65, 105, 225))
        win.blit(position_text, (830, -2))
    elif x >=100 and y >=100:
        position_text = font.render(f"x = {x}, y = {y}", True, (65, 105, 225))
        win.blit(position_text, (805, -2))
    elif x >= 100 or y >= 100:
        position_text = font.render(f"x = {x}, y = {y}", True, (65, 105, 225))
        win.blit(position_text, (817, -2))
    else:
        position_text = font.render(f"x = {x}, y = {y}", True, (65, 105, 225))
        win.blit(position_text, (845, -2))

    # Wyświetlanie wyniku
    score_text = font.render(f"score: {score}", True, (76, 187, 23))
    win.blit(score_text, (2,-2))

    pygame.display.update()

pygame.quit()
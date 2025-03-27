import pygame
import Enemy
import Player

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("myGame")

WHITE = (235, 255, 245)

player_image = pygame.image.load("/Users/lukaszkundzicz/PycharmProjects/Grafika/GraProjekt/images/player")
enemy_image = pygame.image.load("/Users/lukaszkundzicz/PycharmProjects/Grafika/GraProjekt/images/enemy")
background_image = pygame.image.load("/Users/lukaszkundzicz/PycharmProjects/Grafika/GraProjekt/images/background")

time_per_frame = 100

player = Player(100, 400, player_image)
enemy = Enemy(500, 400, enemy_image)

# main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1)
    if keys[pygame.K_RIGHT]:
        player.move(1)
    if keys[pygame.K_SPACE]:
        player.attack(enemy)

    player.draw(screen)
    enemy.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
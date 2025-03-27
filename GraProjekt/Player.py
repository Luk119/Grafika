from GraProjekt.Main import enemy


class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.is_attacking = False

    def move(self, dx):
        if self.rect.colliderect(enemy.rect):
            enemy.take_damage()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
class Enemy:
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.health = 3

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.rect.x = -100
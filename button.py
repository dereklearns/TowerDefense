import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x , y, filepath, istower):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((40, 40))
        #self.image.fill((0,0,0))

        self.image = pygame.image.load(filepath)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.tower = istower

        if istower:
            self.build = filepath


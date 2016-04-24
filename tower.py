import pygame
import math

import projectiles


class Tower(pygame.sprite.Sprite):
    def __init__(self, x , y, towertype):
        pygame.sprite.Sprite.__init__(self)
        self.towertype = towertype
        if towertype == "BasicCannon.png":
            self.image = pygame.image.load("tower.png")
            self.range = 200
            self.maxfirerate = 10
            self.firerate = 0
            self.cost = 50
            self.tooltip = "TOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOLTIP TEST "
        elif towertype == "TOWER2":
            self.image = pygame.image.load("tower2.png")
            self.range = 100
            self.maxfirerate = 3
            self.firerate = 0
            self.cost = 100

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)



    def tower_selected(self, surface):
        pygame.draw.circle(surface, (0,255,0), self.rect.center, 20, 1)
    def draw_tower_range(self, surface):
        pygame.draw.circle(surface,(255,0,0), self.rect.center, self.range, 1)
    def update(self):
        self.firerate += 1
    def shoot(self):
        self.firerate = 0
    def can_shoot(self):
        if self.firerate >= self.maxfirerate:
            return True
        else:
            return False

    def detect_target(self, creep):
        x = self.rect.x - creep.rect.x
        y = self.rect.y - creep.rect.y
        if math.sqrt(x*x + y*y) <= self.range:
            return True
        else:
            return False







import math
import pygame

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return math.atan2(-y_dist, x_dist) % (2 * math.pi)
def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (math.cos(angle) * distance),
            pos[1] - (math.sin(angle) * distance))

def get_distance(origin, destination):
    x = origin[0] - destination[0]
    y = origin[1] - destination[1]
    return math.sqrt(x*x + y*y)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, origin, destination):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = origin
        self.destination = destination
        self.damage = 1
        self.angle = 0
        self.speed = 50
        self.temp = 0
        self.distance = None
    def bullet_stopped(self):

        if self.rect.center == self.destination:
            return True
        else:
            return False

    def update(self):
        self.distance = get_distance(self.rect.center, self.destination)

        self.angle = get_angle(self.rect.center, self.destination)

        self.rect.center = project(self.rect.center, self.angle, min(self.distance,self.speed))

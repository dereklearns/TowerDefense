import pygame
import math
import itertools

def get_distance(origin, destination):
    x = origin[0] - destination[0]
    y = origin[1] - destination[1]
    return math.sqrt(x*x + y*y)

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

class Creep(pygame.sprite.Sprite):

    def __init__(self,pos,hp):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("creep.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp = hp
        self.waypoints = iter([[60,0],[60,220], [260,220],[260,380],[60,380],[60,600]])
        self.distance = 0
        self.destination = next(self.waypoints)
        self.speed = 3
        self.stepstaken = 0
        self.exit = False
        self.reward = 5

    def reached_destination(self):
        if self.rect.center == (self.destination[0],self.destination[1]):
            return True
        else:
            return False

    def update(self):
        self.stepstaken += 1
        if self.reached_destination():

            try:
                self.destination = next(self.waypoints)
            except StopIteration:

                #Reached end of waypoints
                self.exit = True
        self.distance = get_distance(self.rect.center, self.destination)

        self.angle = get_angle(self.rect.center, self.destination)

        self.rect.center = project(self.rect.center, self.angle, min(self.distance,self.speed))


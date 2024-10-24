import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        angle = random.uniform(20, 50)
        self.kill()
        if self.radius == ASTEROID_MIN_RADIUS:
            return
        else:
            velo1 = self.velocity.rotate(angle)
            velo2 = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            aster1 = Asteroid(self.position.x, self.position.y, new_radius)
            aster1.velocity = velo1 * 1.2
            aster2 = Asteroid(self.position.x, self.position.y, new_radius)
            aster2.velocity = velo2 * 1.2
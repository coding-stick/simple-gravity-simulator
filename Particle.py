import pygame
import random

class Particle():
    def __init__(self,pos,radius,color,vel,acc):
        self.pos = pygame.Vector2(pos)
        self.color=color
        self.radius = radius
        self.mass= radius**2

        self.vel = vel # pygame.vector2
        self.acc = acc # pygame.vector2
        self.elasticity = 0.9

    def apply_force(self, force):
        self.acc+=force/self.mass

    def accelerate(self,acc):
        self.acc+=acc

    def update(self,delta):
        self.vel+=self.acc
        self.acc*=0

        self.pos+=self.vel*delta

    def inside(self,other):
        """
            detect if another particle is inside it.
        """
        dist_squared = (self.pos - other.pos).magnitude_squared()
        if 0 < dist_squared < (self.radius + other.radius)**2:
            return True
        else:
            return False

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

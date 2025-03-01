import pygame, random, math
from Particle import Particle
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRav Simulation")

#G = pygame.Vector2(0,0)
g_const = -10
FPS = 60

particle_list = []


def mass_to_rgb(mass):
    '''
    min_mass = 100
    max_mass = 10000

    # Ensure mass is within the expected range
    mass = max(min(mass, max_mass), min_mass)

    normalized_mass = (mass - min_mass) / (max_mass - min_mass)
    
    # Gradient from blue to white to red
    if normalized_mass <= 0.5:
        red = int(255 * normalized_mass * 2)
        green = int(255 * normalized_mass * 2)
        blue = 255
    else:
        red = 255
        green = int(255 * (1 - normalized_mass) * 2)
        blue = int(255 * (1 - normalized_mass) * 2)
    '''
    return "red"



def edge(particle):
    w, h = WIDTH, HEIGHT
    if (particle.pos.x - particle.radius > w) or (particle.pos.x + particle.radius < 0) or (particle.pos.y - particle.radius > h) or (particle.pos.y + particle.radius < 0):
        return True
    return False

def main():
    running = True
    clock = pygame.time.Clock()
    growing = False
    spawn_radius = 1
    new_radius = 1

    while running:
        delta = clock.tick(FPS) / 1000
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                growing = True
            elif event.type == MOUSEBUTTONUP:
                growing = False
                new_particle = Particle(mouse_pos, spawn_radius, mass_to_rgb(spawn_radius**2), pygame.Vector2(0, 0), pygame.Vector2(0, 0))
                particle_list.append(new_particle)
                spawn_radius = 1
        
        if growing:
            pygame.draw.circle(win, mass_to_rgb(spawn_radius**2), mouse_pos, spawn_radius)
            spawn_radius += 1

        for i, p in enumerate(particle_list):
            g_force = pygame.Vector2(0, 0)
            for p2 in particle_list[i+1:]:
                if (p.inside(p2)):
                    new_mass = p.mass + p2.mass
                    new_radius = (new_mass ** 0.5)  # Since radius squared gives mass
                    new_color = mass_to_rgb(new_mass)
                    
                    # Center of mass calculation
                    new_pos = (p.pos * p.mass + p2.pos * p2.mass) / new_mass
                    new_vel = (p.vel * p.mass + p2.vel * p2.mass) / new_mass

                    replace_particle = Particle(new_pos, new_radius, new_color, new_vel, p.acc + p2.acc)
                    particle_list.append(replace_particle)
                    particle_list.remove(p)
                    particle_list.remove(p2)
                else:
                    dist = math.sqrt((p.pos.x - p2.pos.x) ** 2 + (p.pos.y - p2.pos.y) ** 2)
                    if dist == 0:
                        continue
                    angle = math.atan2((p.pos.y - p2.pos.y), (p.pos.x - p2.pos.x))
                    g_force += (g_const * p.mass * p2.mass / (dist) ** 2) * pygame.Vector2(math.cos(angle), math.sin(angle))

            if edge(p):
                particle_list.remove(p)

            p.apply_force(g_force)
            p.update(delta)
            p.draw(win)

        pygame.display.update()
        win.fill("black")

    pygame.quit()

if __name__ == "__main__":
    main()

import math
import random

import pygame
from pygame.math import Vector2

FPS = 60
SIZE = 500
MAX_MOVES = 500
START = (30, 30)
GOAL = (450, 450)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Karaluch")
clock = pygame.time.Clock()

class Dot(pygame.sprite.Sprite):
    def __init__(self, moves):
        pygame.sprite.Sprite.__init__(self)
        self.step = 0
        self.dead = False
        self.done = False
        self.pos = Vector2(START[0], START[1])
        self.vel = Vector2(0.0, 0.0)
        self.acc = Vector2(0.0, 0.0)
        self.moves = moves

        self.image = pygame.Surface((2, 2), pygame.SRCALPHA)
        self.org_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.image.fill((255, 0, 0))

    def move(self):
        if self.dead or self.done:
            return

        acc = self.moves[self.step]
        self.acc += acc
        self.vel += self.acc
        if (self.vel.length() > 5):
            self.vel.scale_to_length(5)
        self.pos += self.vel
        self.step += 1

        if self.pos.x < 0 or self.pos.x >= SIZE - 1:
            self.dead = True
            self.vel = Vector2(0,0)

        if self.pos.y < 0 or self.pos.y >= SIZE - 1:
            self.dead = True
            self.vel = Vector2(0, 0)

        if self.pos.x > GOAL[0] - 10 and self.pos.x < GOAL[0] + 10  and \
            self.pos.y > GOAL[1] - 10 and self.pos.y < GOAL[1] + 10:
            self.done = True
            self.dead = True

    def update(self, *args):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.dead:
            self.image.fill((255,0,0))
        else:
            self.image.fill((0,0,0))


class Population(pygame.sprite.Group):
    def __init__(self, size):
        self.dots = []
        pygame.sprite.Group.__init__(self)
        for i in range(size):
            moves = []
            for a in range(1000):
                rad = math.radians(random.randrange(0, 360))
                v = Vector2()
                v.x = math.cos(rad)
                v.y = math.sin(rad)
                moves.append(v)
            dot = Dot(moves)
            self.dots.append(dot)
            self.add(dot)


    def move(self):
        for dot in self.dots:
            dot.move()

population = Population(1000)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    population.move()
    population.update()
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255,255,0), (450, 450), 10)
    pygame.draw.circle(screen, (0,0,255), (30, 30), 10)
    population.draw(screen)
    pygame.display.flip()
    #pygame.time.delay(100)

pygame.quit()
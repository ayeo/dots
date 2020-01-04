import math
import random
import numpy as np

import pygame
from pygame.math import Vector2

FPS = 60
SIZE = 500
MAX_MOVES = 1500
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
        self.moves = moves.copy()

        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        self.org_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.image.fill((255, 0, 0))

    def move(self, best):
        if self.dead or self.done:
            return

        acc = self.moves[self.step]
        self.acc += acc
        self.vel += self.acc
        if (self.vel.length() > 2):
            self.vel.scale_to_length(2)
        self.pos += self.vel
        self.step += 1

        # if self.step > best:
        #     self.dead = True
        #     self.vel = Vector2(0, 0)

        if (self.step >= MAX_MOVES):
            self.dead = True
            self.vel = Vector2(0, 0)

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

        #(0, 120, 300, 20))
        if self.pos.x >  0 and self.pos.x < 300  and \
            self.pos.y > 120 and self.pos.y < 150:
            self.dead = True

        #(300, 250, 200, 20))
        if self.pos.x > 300 and self.pos.x < 500  and \
            self.pos.y > 250 and self.pos.y < 270:
            self.dead = True

    def update(self, *args):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.dead:
            self.image.fill((255,0,0))
        else:
            self.image.fill((0,0,0))

    def distance(self):
        a = math.pow(self.pos.x - GOAL[0], 2)
        b = math.pow(self.pos.y - GOAL[1], 2)
        return math.sqrt(a + b)


    def fitness(self):
        if self.done:
            return 1 + (1.0 / (self.step * self.step)) * 10000
        else:
            return (1 / (self.distance() * self.distance())) * 100

    def clone(self):
        return Dot(self.moves)

    def mutate(self):
        factor = 0.01
        for i in range(len(self.moves)):
            if random.random() < factor:
                r = random.randrange(0, 360)
                v = Vector2(2, 0)
                v = v.rotate(r)
                self.moves[i] = v


class Population(pygame.sprite.Group):
    def __init__(self, size):
        self.dots = []
        self.best = MAX_MOVES * 2
        pygame.sprite.Group.__init__(self)
        for i in range(size):
            moves = []
            for a in range(1000):
                r = random.randrange(0, 360)
                v = Vector2(2, 0)
                v = v.rotate(r)
                moves.append(v)
            dot = Dot(moves)
            self.dots.append(dot)
            self.add(dot)

    def move(self):
        for dot in self.dots:
            dot.move(self.best)
            if dot.done:
                self.best = min(self.best, dot.step)

    def all_dead(self):
        for dot in self.dots:
            if dot.dead == False:
                return False
        return True

    def build_weights(self, population):
        weights = []
        for dot in population:
            weights.append(dot.fitness())
        weights = [float(i)/sum(weights) for i in weights]
        return weights

    def mutate(self):
        elite = sorted(self.dots, key=lambda x: -1 * x.fitness())
        elite = elite[:200]
        new_population = []

        for i in range(10):
            new_population.append(elite[i]) # the best
        # for e in elite:
        #     new_population.append(e.clone())

        for i in range(999):
            new_dot = np.random.choice(elite, p=self.build_weights(elite)).clone()
            new_dot.mutate()
            new_population.append(new_dot)

        self.empty()
        self.dots = new_population
        for dot in self.dots:
            self.add(dot)

population = Population(5000)

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
    pygame.draw.rect(screen, (222,222,222), (0, 120, 300 ,20))
    pygame.draw.rect(screen, (222,222,222), (300, 250, 200, 20))
    population.draw(screen)
    pygame.display.flip()
    #pygame.time.delay(100)

    if population.all_dead():
        population.mutate()

pygame.quit()
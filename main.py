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
    def __init__(self, moves, is_best=False):
        pygame.sprite.Sprite.__init__(self)
        self.step = 0
        self.dead = False
        self.is_best = is_best
        self.done = False
        self.pos = Vector2(START[0], START[1])
        self.vel = Vector2(0.0, 0.0)
        self.acc = Vector2(0.0, 0.0)
        self.moves = moves.copy()

        self.image = pygame.Surface((2, 2), pygame.SRCALPHA)
        if is_best:
            self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
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
        if (self.vel.length() > 5):
            self.vel.scale_to_length(5)
        self.pos += self.vel
        self.step += 1

        if self.step > best + 20:
            self.dead = True
            self.vel = Vector2(0, 0)

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
            self.pos.y > 120 and self.pos.y < 140:
            self.dead = True

        #(200, 250, 300, 20))
        if self.pos.x > 200 and self.pos.x < 500  and \
            self.pos.y > 250 and self.pos.y < 270:
            self.dead = True

    def update(self, *args):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.is_best:
            self.image.fill((0,255,0))
        elif self.dead:
            self.image.fill((150,150,150))
        else:
            self.image.fill((0,0,0))

    def distance(self):
        a = math.pow(self.pos.x-GOAL[0],2)
        b = math.pow(self.pos.y-GOAL[1],2)
        return math.sqrt(a + b)


    def fitness(self):
        if self.done:
            return 1.0 / 16.0 + 10000.0 / (float)(self.step * self.step)
        else:
            return 1.0 / (self.distance() * self.distance())

    def clone(self, is_best=False):
        return Dot(self.moves, is_best)

    def mutate(self):
        factor = 0.01

        clone = self.clone()
        for i in range(len(self.moves)):
            if random.random() < factor:
                r = random.randrange(0, 360)
                v = Vector2(5, 0)
                v = v.rotate(r)
                v = v.normalize()
                clone.moves[i] = v

        return clone


class Population(pygame.sprite.Group):
    def __init__(self, size):
        self.dots = []
        self.best = MAX_MOVES * 2
        pygame.sprite.Group.__init__(self)
        for i in range(size):
            moves = []
            for a in range(1000):
                r = random.randrange(0, 360)
                v = Vector2(5, 0)
                v = v.rotate(r)
                v = v.normalize()
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

    def total_fitness(self):
        sum = 0
        for dot in self.dots:
            sum += dot.fitness()
        return sum

    def select_parent(self, sum):
        rand = random.uniform(0, sum)
        runningSum = 0
        for i in range(len(self.dots)):
            runningSum += self.dots[i].fitness()
            if runningSum > rand:
                return self.dots[i];

    def mutate(self):
        elite = sorted(self.dots, key=lambda x: -1 * x.fitness())
        elite = elite[:10]
        new_population = []

        sum = self.total_fitness()
        for i in range(999):
            new_dot = self.select_parent(sum)
            new_dot = new_dot.mutate()
            new_population.append(new_dot)

        e = elite[0].clone(True)  # the best
        new_population.append(e)

        self.empty()
        self.dots = new_population
        for dot in self.dots:
            self.add(dot)

population = Population(3000)

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
    pygame.draw.rect(screen, (222,222,222), (200, 250, 300, 20))
    population.draw(screen)
    pygame.display.flip()
    #pygame.time.delay(100)

    if population.all_dead():
        population.mutate()

pygame.quit()
import math
import random
import numpy as np

import pygame
from pygame.math import Vector2

FPS = 60
SIZE = 500
MAX_MOVES = 1500
START = (250, 50)
GOAL = (250, 450)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Dots Swarm Invasion")
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

        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        if is_best:
            self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
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

        if self.pos.x >  0 and self.pos.x < 300  and \
            self.pos.y > 150 and self.pos.y < 170:
            self.dead = True

        if self.pos.x > 200 and self.pos.x < 500  and \
            self.pos.y > 300 and self.pos.y < 320:
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
            return 1 + 1.0 /self.step
        else:
            return 1 / self.distance()

    def clone(self, is_best=False):
        return Dot(self.moves, is_best)

    def mutate(self, steps=3):
        clone = self.clone()
        while steps >= 0:
            r = random.randrange(0, 360)
            v = Vector2(1, 0)
            v = v.rotate(r)
            v = v.normalize()
            i = random.randint(0, len(clone.moves)-1)
            clone.moves[i] = v
            steps -= 1

        return clone


class Population(pygame.sprite.Group):
    def __init__(self, size):
        self.dots = []
        self.best = MAX_MOVES
        pygame.sprite.Group.__init__(self)
        for i in range(size):
            moves = []
            for a in range(1000):
                r = random.randrange(0, 360)
                v = Vector2(1, 0)
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
        sum_w = sum(weights)
        weights = [i/sum_w for i in weights]
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
                return self.dots[i]

    def mutate(self):
        elite = sorted(self.dots, key=lambda x: -1 * x.fitness())
        elite = elite[:200]
        new_population = []
        for i in range(999):
            new_dot = np.random.choice(elite, p=self.build_weights(elite))
            if new_dot.done:
                new_dot = new_dot.mutate(3)
            else:
                new_dot = new_dot.mutate(15)
            new_population.append(new_dot)
        new_population.append(elite[0].clone(True))  # the best
        self.empty()
        self.dots = new_population
        for dot in self.dots:
            self.add(dot)

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
    pygame.draw.rect(screen, (100,100,100), (GOAL[0]-10, GOAL[1]-10, 20, 20))
    pygame.draw.rect(screen, (100,100,100), (START[0]-10, START[1]-10, 20, 20))
    pygame.draw.rect(screen, (222,222,222), (0, 150, 300 ,20))
    pygame.draw.rect(screen, (222,222,222), (200, 300, 300, 20))
    population.draw(screen)
    pygame.display.flip()
    #pygame.time.delay(100)

    if population.all_dead():
        population.mutate()

pygame.quit()
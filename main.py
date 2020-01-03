import math
import random

import pygame

FPS = 60
SIZE = 500
MAX_MOVES = 500

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Karaluch")
clock = pygame.time.Clock()

class Dot(pygame.sprite.Sprite):
    def __init__(self, position, moves, angle):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.dead = False
        self.done = False
        self.moves = moves.copy()
        self.image = pygame.Surface((4, 8), pygame.SRCALPHA)
        self.org_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.total = 0
        self.org_pos = position

        self.angle = angle
        self.init_angle = angle

    def clone(self):
        x = Dot(self.org_pos, self.moves.copy(), self.init_angle)
        return x

    def distance(self, point):
        a = math.pow(point[0] - self.rect.x, 2)
        b = math.pow(point[1] - self.rect.y, 2)
        return math.sqrt(a + b)

    # def cross(self, other):
    #     moves = self.moves[:int(MAX_MOVES/2)] + other.moves[:-1*int(MAX_MOVES/2)]
    #     x = Dot(self.org_pos, moves)
    #     x.angle = self.init_angle
    #     return x

    def fitness(self):
        if (self.done):
            return 1 / self.total
        else:
            return 2 - 1 / self.distance((450, 450))

    def mutate(self):
        factor = .0001
        for i in range(len(self.moves)):
            if random.random() < factor:
                self.moves[i] = random.randint(-40, 40)

    def update(self, *args):
        self.org_image.fill((255, 255, 255))
        if (self.dead):
            self.org_image.fill((255, 0, 0))
        if (self.done):
            self.org_image.fill((255, 255, 0))

        self.image = pygame.transform.rotate(self.org_image, 90 - self.angle)


    def move(self):
        if self.dead or self.done:
            return

        angle = self.moves[self.total]
        self.angle += angle
        radians = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radians)
        self.rect.y += self.speed * math.sin(radians)

        self.total += 1

        if (self.total == MAX_MOVES):
            self.dead = True

        if self.rect.x <= -5 or self.rect.x >= SIZE - 5:
            self.dead = True
        if self.rect.y <= -5 or self.rect.y >= SIZE - 5:
            self.dead = True

        if self.rect.x > 440 and self.rect.x < 460 and self.rect.y > 440 and self.rect.y < 460:
            self.done = True
            self.dead = True


class Population(pygame.sprite.Group):
    size = 1000
    dots = []

    def move(self):
        for dot in self.dots:
            dot.move()

    def start(self, pos):
        for i in range(self.size):
            moves = [random.randint(-40,40) for i in range(MAX_MOVES)]
            dot = Dot(pos, moves.copy(), random.randint(0, 360))
            self.dots.append(dot)
            self.add(dot)

    def kill_all(self):
        for i in self.dots:
            i.dead = True

    def random_pair(self, max: int) -> (Dot, Dot):
        a = b = random.randint(0, max)
        while (a == b):
            b = random.randint(0, max)
        return (self.dots[a], self.dots[b])

    def crossover(self, max, population):
        a = population[random.randint(0, max)]
        crossed = a.clone() #.cross(b)
        crossed.mutate()

        return crossed

    def all_dead(self):
        for dot in self.dots:
            if dot.dead == False:
                return False
        return True

    def mutate(self):
        new_dots = sorted(self.dots, key=lambda x: x.fitness())
        dots = []
        for i in range(50):
            dots.append(new_dots[i].clone())

        for x in range(950):
            dots.append(self.crossover(20, new_dots))

        self.dots = dots
        self.empty()
        for i in self.dots:
            self.add(i)

population = Population()
population.start((random.randint(20,40),random.randint(20,40)))

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    population.move()
    population.update()
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255,255,0), (450, 450), 10)
    pygame.draw.circle(screen, (0,0,255), (30, 30), 10)
    population.draw(screen)
    pygame.display.flip()
    pygame.time.delay(10)

    if population.all_dead():
        population.mutate()

pygame.quit()
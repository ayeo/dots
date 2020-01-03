import math
from random import randint

import pygame
from pygame.math import Vector2

FPS = 60
SIZE = 300
TAIL = 2
ANTS = 20

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SIZE * TAIL, SIZE * TAIL))
pygame.display.set_caption("Karaluch")
clock = pygame.time.Clock()

class Dot(pygame.sprite.Sprite):
    actions = [0, -20, 20]
    angle = 0
    speed = 5

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((5, 10), pygame.SRCALPHA)
        self.org_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.image.fill((255, 255, 0))
        # self.velocity = Vector2(1, 0)


    def update(self, *args):
        self.image = pygame.transform.rotate(self.org_image, 90 - self.angle)

    def move(self, action):
        angle = self.actions[action]

        self.angle += angle
        radians = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radians)
        self.rect.y += self.speed * math.sin(radians)



all_sprites = pygame.sprite.Group()
dot = Dot((150, 150))
all_sprites.add(dot)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dot.move(randint(0, 2))
    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
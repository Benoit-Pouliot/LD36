import math
import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.settings import *


class EnemyWalkman(Enemy):
    def __init__(self, x, y, direction="Right"):
        super().__init__(x, y, os.path.join('img', 'enemyWalkman.png'))

        self.name = "enemyCactus"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'enemyWalkman.png'))
        self.image = self.imageEnemy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.initx = self.rect.x
        self.inity = self.rect.y

        self.speedBase = 1
        self.distanceMax = 200

        self.speedx = self.speedBase
        self.speedy = 0
        self.distance = 0

        self.direction = direction
        if self.direction == "Left":
            self.speedx = -self.speedBase
        if self.direction == "Right":
            self.speedx = self.speedBase

        self.isGravityApplied = True
        self.isCollisionApplied = True

    def set_direction(self, direction):
        self.direction = direction
        if self.direction == "Left":
            self.speedx = -self.speedBase
        if self.direction == "Right":
            self.speedx = self.speedBase

    def set_distance_max(self, distance):
        self.distanceMax = distance

    def update(self):

        if self.speedx == 0 or self.distance >= self.distanceMax:
            if self.direction == "Right":
                self.direction = "Left"
                self.speedx = -self.speedBase
            elif self.direction == "Left":
                self.direction = "Right"
                self.speedx = self.speedBase

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # print(self.speedy)

        self.distance = math.fabs(self.initx - self.rect.x)

    def dead(self):
        self.soundDead.play()
        self.kill()

    def spring(self):
        self.speedy = -15
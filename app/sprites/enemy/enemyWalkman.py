import math
import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.settings import *
from app.sprites.collisionMask import CollisionMask


class EnemyWalkman(Enemy):
    def __init__(self, x, y, direction="Right"):
        super().__init__(x, y, os.path.join('img', 'enemyWalkman.png'))

        self.name = "enemyWalkman"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.initx = self.rect.x
        self.inity = self.rect.y

        self.speedBase = 2
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

        self.life = 3

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

        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

        self.distance = math.fabs(self.initx - self.rect.x)

    def spring(self):
        self.speedy = -15

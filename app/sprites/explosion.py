__author__ = 'Bobsleigh'

import pygame
import os
from app.settings import *
from app.tools.counter import Counter
from app.sprites.collisionMask import CollisionMask

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, friendly=True):
        super().__init__()

        self.name = "explosion"

        self.image = pygame.Surface((60,60))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = 0
        pygame.draw.circle(self.image, RED, (int(self.rect.width/2),int(self.rect.height/2)), 30, 10)

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.animation = None

        self.friendly = friendly
        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = True

        self.jumpState = JUMP

        self.facingSide = RIGHT

        self.counter = Counter()
        self.duration = 30 #In frames

    def update(self):
        self.counter.count()
        if self.counter.value >= self.duration:
            self.kill()

    def detonate(self):
        pass

    def dead(self):
        pass

    def spring(self):
        pass
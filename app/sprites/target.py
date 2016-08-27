__author__ = 'Bobsleigh'

import pygame
import os
from app.settings import *

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(os.path.join('img', 'biere32x32-4.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0
        self.speedy = 0

        self.isPhysicsApplied = False
        self.isGravityApplied = True
        self.isFrictionApplied = True
        self.isCollisionApplied = True

        self.jumpState = JUMP

        self.facingSide = RIGHT

        self.powerx = 0
        self.powery = 0

    def dead(self):
        pass

    def spring(self):
        pass
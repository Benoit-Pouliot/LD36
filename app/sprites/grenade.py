__author__ = 'Bobsleigh'


import os
import pygame
from app.settings import JUMP

from app.scene.platformScreen.collisionPlayerPlatform import *
# from app.tool.animation import Animation


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, speedX, speedY, friendly=True):
        super().__init__()

        self.name = "grenade"
        self.speedx = speedX
        self.speedy = speedY

        image1 = pygame.image.load(os.path.join('img', 'biere32x32.png'))
        image2 = pygame.image.load(os.path.join('img', 'biere32x32-2.png'))
        image3 = pygame.image.load(os.path.join('img', 'biere32x32-3.png'))
        image4 = pygame.image.load(os.path.join('img', 'biere32x32-4.png'))
        self.frames = [image1,image2,image3,image4]
        self.image = self.frames[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.animation = None

        self.friendly = friendly
        self.isPhysicsApplied = False
        self.isGravityApplied = True
        self.isFrictionApplied = True
        self.isCollisionApplied = True

        self.jumpState = JUMP

        self.facingSide = RIGHT

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def dead(self):
        self.kill()
__author__ = 'Bobsleigh'

import os
import pygame
from app.settings import JUMP
from app.sprites.explosion import Explosion

from app.scene.platformScreen.collisionPlayerPlatform import *
from app.sprites.collisionMask import CollisionMask
# from app.tool.animation import Animation


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, speedX, speedY, mapData, friendly=True):
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
        self.rect.centerx = x
        self.rect.centery = y
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.animation = None

        self.friendly = friendly
        self.isPhysicsApplied = False
        self.isGravityApplied = True
        self.isFrictionApplied = False
        self.isCollisionApplied = True

        self.jumpState = JUMP

        self.facingSide = RIGHT

        self.mapData = mapData

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.collisionMask.rect = self.rect

    def dead(self):
        self.kill()

    def spring(self):
        pass

    def detonate(self):
        self.kill()

        explosion = Explosion(self.rect.midbottom[0], self.rect.midbottom[1])

        self.mapData.camera.add(explosion)
        self.mapData.allSprites.add(explosion)
        self.mapData.friendlyExplosion.add(explosion)

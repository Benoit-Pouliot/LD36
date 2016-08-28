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

        self.frames = list()
        self.frames.append(pygame.image.load(os.path.join('img', 'cursor_v3.png')))
        for k in range(1, 36):
            self.frames.append(pygame.transform.rotate(self.frames[0], -k*10))
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

        self.imageIter = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.collisionMask.rect = self.rect

        self.imageIter = (self.imageIter+1) % len(self.frames)
        self.image = self.frames[self.imageIter]

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

import pygame
import os

from app.sprites.collisionMask import CollisionMask
from app.settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, pathImage=os.path.join('img', 'Cochon.png')):
        super().__init__()

        self.name = "enemy"

        # self.image = pygame.transform.scale(pygame.image.load(image), (TILEDIMX, TILEDIMY))
        self.image = pygame.image.load(pathImage)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collisionMask = CollisionMask(0,0,0,0)
        self.collisionMask.rect = self.rect


        self.jumpState = JUMP
        self.specialState = None
        self.specialWallSide = None
        self.shape = None

        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False

        self.soundDead = pygame.mixer.Sound(os.path.join('music_pcm', 'Punch2.wav'))
        self.soundDead.set_volume(1)

    def update(self):
        self.collisionMask.rect = self.rect

    def detonate(self):
        pass

    def hurt(self):
        pass

    def dead(self):
        self.soundDead.play()
        self.kill()
import pygame
import os

from app.sprites.collisionMask import CollisionMask
from app.settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, pathImage=os.path.join('img', 'Cochon.png')):
        super().__init__()

        self.name = "enemy"

        # self.image = pygame.transform.scale(pygame.image.load(image), (TILEDIMX, TILEDIMY))
        self.imageEnemy = pygame.image.load(pathImage)
        self.image = self.imageEnemy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collisionMask = CollisionMask(0,0,0,0)
        self.collisionMask.rect = self.rect

        self.imageTransparent = pygame.Surface((1,1))
        self.imageTransparent.set_colorkey(BLACK)

        self.jumpState = JUMP
        self.specialState = None
        self.specialWallSide = None
        self.shape = None

        self.isInvincible = False
        self.invincibleFrameCounter = 0
        self.invincibleFrameDuration = 60

        self.isPhysicsApplied = False
        self.isGravityApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False

        self.soundDead = pygame.mixer.Sound(os.path.join('music_pcm', 'Punch2.wav'))
        self.soundDead.set_volume(1)

    def update(self):
        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

    def invincibleUpdate(self):
        if self.invincibleFrameCounter > 0 and self.invincibleFrameCounter < self.invincibleFrameDuration:
            self.invincibleFrameCounter += 1
        elif self.invincibleFrameCounter == self.invincibleFrameDuration:
            self.isInvincible = False
            self.invincibleFrameCounter = 0
        self.visualFlash()


    def detonate(self):
        pass

    def hurt(self):
        if not self.isInvincible:
            self.life -= 1
            if self.life <= 0:
                self.dead()
            self.invincibleOnHit()
            self.visualFlash()

    def dead(self):
        self.soundDead.play()
        self.kill()

    def visualFlash(self):
        if self.invincibleFrameCounter == 1:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 5:
            self.image = self.imageEnemy
        elif self.invincibleFrameCounter == 15:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 20:
            self.image = self.imageEnemy
        elif self.invincibleFrameCounter == 30:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 35:
            self.image = self.imageEnemy
        elif self.invincibleFrameCounter == 45:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 50:
            self.image = self.imageEnemy

    def invincibleOnHit(self):
        self.isInvincible = True
        self.invincibleFrameCounter = 1
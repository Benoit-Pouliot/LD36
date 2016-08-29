import pygame
import os
import random

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import WordBulletDiag
from app.settings import *
from app.sprites.collisionMask import CollisionMask

class EnemyPhone(Enemy):
    def __init__(self, x, y, theMap, iterStart=0):
        super().__init__(x, y, os.path.join('img', 'EnemyPhone.png'))

        self.name = "EnemyPhone"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.speedx = 0
        self.speedy = 0

        self.theMap = theMap

        self.isGravityApplied = False
        self.isCollisionApplied = False

        self.imageIterShoot = 40
        self.imageWaitNextShoot = 80
        self.imagePhoneNumber = -1

        self.isInvincible = True
        self.isShooter = 0

        self.fallSpd = 6

        self.life = 1

    def update(self):

        if self.isShooter == 1:
             self.imageIterShoot += 1
             if self.imageIterShoot > self.imageWaitNextShoot:

                 self.imageIterShoot = 0

                 random.seed()
                 if random.randint(1, 2) == 1:
                     bullet = WordBulletDiag(self.rect.x+32, self.rect.y+1, RIGHT, -90, False)
                 else:
                     bullet = WordBulletDiag(self.rect.x+32+32, self.rect.y+1, LEFT, -90, False)

                 self.theMap.camera.add(bullet)
                 self.theMap.allSprites.add(bullet)
                 self.theMap.enemyBullet.add(bullet)

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

    def fallDown(self):
        self.speedy = self.fallSpd
        self.isGravityApplied = True
        self.isCollisionApplied = True
        self.invincibleFrameCounter = 1
        self.imagePhoneNumber = -1
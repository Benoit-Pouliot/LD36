import pygame
import os
import random

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import NoteBulletDiag
from app.settings import *

class EnemyNoteInv(Enemy):
    def __init__(self, x, y, theMap, iterStart=0):
        super().__init__(x, y, os.path.join('img', 'enemyNoteInv.png'))

        self.name = "enemyNoteInv"

        self.speedx = 0
        self.speedy = 0

        self.theMap = theMap

        self.isGravityApplied = False
        self.isCollisionApplied = False

        self.imageIterShoot = iterStart
        self.imageWaitNextShoot = list()
        self.imageWaitNextShoot.append(680)
        self.imageWaitNextShoot.append(700)
        self.imageWaitNextShoot.append(720)
        self.imageIterWaitNextShoot = 0
        self.imageIterWaitNextShootMax = len(self.imageWaitNextShoot)

    def update(self):

        self.imageIterShoot = min(self.imageIterShoot+1, 2*self.imageWaitNextShoot[self.imageIterWaitNextShootMax-1])
        if self.imageIterShoot > self.imageWaitNextShoot[self.imageIterWaitNextShoot]:

            self.imageIterWaitNextShoot += 1
            if self.imageIterWaitNextShoot == self.imageIterWaitNextShootMax:
                self.imageIterWaitNextShoot = 0
                self.imageIterShoot = 0

            random.seed()
            if random.randint(1, 2) == 1:
                bullet = NoteBulletDiag(self.rect.x, self.rect.y+1, RIGHT, -90, False)
            else:
                bullet = NoteBulletDiag(self.rect.x+32, self.rect.y+1, LEFT, -90, False)

            self.theMap.camera.add(bullet)
            self.theMap.allSprites.add(bullet)
            self.theMap.enemyBullet.add(bullet)




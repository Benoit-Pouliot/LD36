import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import BeerBullet
from app.tools.animation import Animation

from app.settings import *
import random


class EnemyShooter(Enemy):
    def __init__(self, x, y, theMap, direction="Right"):
        super().__init__(x, y)

        self.name = "enemyShooter"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'enemybob.png'))

        self.imageEnemy2 = pygame.image.load(os.path.join('img', 'enemybob2.png'))
        self.imageEnemy3 = pygame.image.load(os.path.join('img', 'enemybob3.png'))
        self.frames = [self.imageEnemy,self.imageEnemy2,self.imageEnemy3]
        self.animation = Animation(self,self.frames,20)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0
        self.speedy = 0

        self.theMap = theMap

        self.setDirection(direction)

        self.isGravityApplied = True
        self.isCollisionApplied = True

        self.imageIterShoot = random.randint(10,70)
        self.imageWaitNextShoot = 80

    def setDirection(self, direction):
        self.direction = direction

    def update(self):

        self.animation.update(self)

        self.imageIterShoot += 1
        if self.imageIterShoot > self.imageWaitNextShoot:

            if self.direction == "Right":
                bullet = BeerBullet(self.rect.x + self.rect.width + 1, self.rect.centery, RIGHT, False)
            elif self.direction == "Left":
                bullet = BeerBullet(self.rect.x - 1, self.rect.centery, LEFT, False)

            self.theMap.camera.add(bullet)
            self.theMap.allSprites.add(bullet)
            self.theMap.enemyBullet.add(bullet)

            self.imageIterShoot = 0


        self.rect.x += self.speedx
        if self.speedy < 15:
            self.rect.y += self.speedy

    def dead(self):
        self.soundDead.play()
        self.kill()
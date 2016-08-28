import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import NoteBullet
from app.settings import *
from app.sprites.collisionMask import CollisionMask

class EnemyRadio(Enemy):
    def __init__(self, x, y, theMap, direction="Left"):
        super().__init__(x, y, os.path.join('img', 'enemyRadio.png'))

        self.name = "enemyRadio"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.imageEnemyLeft = pygame.image.load(os.path.join('img', 'enemyRadio.png'))
        self.imageEnemyRight = pygame.transform.flip(self.imageEnemyLeft, True, False)

        self.speedx = 0
        self.speedy = 0

        self.theMap = theMap

        self.setDirection(direction)

        self.isGravityApplied = True
        self.isCollisionApplied = True

        self.imageIterShoot = 40
        self.imageWaitNextShoot = 80

        self.life = 1

    def setDirection(self, direction):
        self.direction = direction
        if self.direction == "Right":
            self.image = self.imageEnemyRight
        if self.direction == "Left":
            self.image = self.imageEnemyLeft

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.collisionMask.rect = self.rect

        self.imageIterShoot = min(self.imageIterShoot+1, 2*self.imageWaitNextShoot)
        if self.imageIterShoot > self.imageWaitNextShoot:

            if self.direction == "Right":
                bullet = NoteBullet(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, False)
            elif self.direction == "Left":
                bullet = NoteBullet(self.rect.x -1, self.rect.centery, LEFT, False)

            self.theMap.camera.add(bullet)
            self.theMap.allSprites.add(bullet)
            self.theMap.enemyBullet.add(bullet)

            self.imageIterShoot = 0

    def hurt(self):
        self.life -= 1
        if self.life <= 0:
            self.dead()



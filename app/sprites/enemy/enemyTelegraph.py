import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import WordBulletDiag
from app.settings import *
from app.sprites.collisionMask import CollisionMask

class EnemyTelegraph(Enemy):
    def __init__(self, x, y, theMap, direction="Left"):
        super().__init__(x, y, os.path.join('img', 'enemyTelegraph.png'))

        self.name = "enemyTelegraph"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.imageEnemyLeft = self.image
        self.imageEnemyLeftAnim = pygame.image.load(os.path.join('img', 'enemyTelegraphAnim.png'))

        self.imageEnemyRight = pygame.transform.flip(self.imageEnemyLeft, True, False)
        self.imageEnemyRightAnim = pygame.transform.flip(self.imageEnemyLeftAnim, True, False)

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
            image2 = self.imageEnemyRightAnim
        if self.direction == "Left":
            self.image = self.imageEnemyLeft
            image2 = self.imageEnemyRightAnim
        image1 = self.image

        self.animation.setAnimation([image1, image2, image1, image2, image1, image2, image1, image2, image1, image1,
                                     image2, image1, image1, image2, image1, image2, image2, image1, image2, image1,
                                     image2, image1, image1], 5)

    def update(self):
        self.animation.update(self)

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

        self.imageIterShoot = min(self.imageIterShoot+1, 2*self.imageWaitNextShoot)
        if self.imageIterShoot > self.imageWaitNextShoot:

            if self.direction == "Right":
                bullet = WordBulletDiag(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, False)
            elif self.direction == "Left":
                bullet = WordBulletDiag(self.rect.x -1, self.rect.centery, LEFT, False)

            self.theMap.camera.add(bullet)
            self.theMap.allSprites.add(bullet)
            self.theMap.enemyBullet.add(bullet)

            self.imageIterShoot = 0



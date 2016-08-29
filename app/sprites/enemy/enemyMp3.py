import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import NoteBullet
from app.settings import *
from app.sprites.collisionMask import CollisionMask

class EnemyMp3(Enemy):
    def __init__(self, x, y, theMap, direction="Left"):
        super().__init__(x, y, os.path.join('img', 'enemyMp3.png'))

        self.name = "enemyMp3"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.speedx = 0
        self.speedy = 0
        self.jumpSpeed = -60

        self.theMap = theMap

        self.direction = direction

        self.isGravityApplied = True
        self.isCollisionApplied = True

        self.imageIterShoot = 40
        self.imageWaitNextShoot = 80

        self.life = 2

        # For animation purpose, sete multiple image
        image1 = self.image
        image2 = pygame.image.load(os.path.join('img', 'enemyMp3Anim.png'))
        image3 = pygame.image.load(os.path.join('img', 'enemyMp3Anim2.png'))
        image4 = pygame.image.load(os.path.join('img', 'enemyMp3Anim3.png'))

        self.animation.setAnimation([image1, image2, image3, image4], 30)

    def update(self):
        self.animation.update(self)

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

        self.imageIterShoot = min(self.imageIterShoot+1, 2*self.imageWaitNextShoot)
        if self.imageIterShoot > self.imageWaitNextShoot:

            bullet1 = NoteBullet(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, False)
            bullet2 = NoteBullet(self.rect.x -1, self.rect.centery, LEFT, False)

            self.theMap.camera.add(bullet1)
            self.theMap.allSprites.add(bullet1)
            self.theMap.enemyBullet.add(bullet1)
            self.theMap.camera.add(bullet2)
            self.theMap.allSprites.add(bullet2)
            self.theMap.enemyBullet.add(bullet2)

            self.imageIterShoot = 0

        if self.speedy == 0 and self.imageIterShoot > self.imageWaitNextShoot*.9:
            self.rect.y += self.jumpSpeed


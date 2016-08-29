import math
import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.settings import *
from app.sprites.collisionMask import CollisionMask
from app.sprites.bullet import WordBulletDiag


class EnemyCommBoss(Enemy):
    def __init__(self, x, y, theMap):
        super().__init__(x, y, os.path.join('img', 'enemyCommBoss.png'))

        self.name = "enemyCommBoss"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.initx = self.rect.x
        self.inity = self.rect.y

        self.theMap = theMap

        self.speedBase = 5
        self.distanceMax = 450

        self.speedx = 0
        self.speedy = -self.speedBase
        self.distance = 0
        self.direction = "Up"

        self.isGravityApplied = False
        self.isCollisionApplied = True

        self.soundVictory = pygame.mixer.Sound(os.path.join('music_pcm', 'levelWin.wav'))

        self.life = 10

        # For animation purpose, sete multiple image
        image1 = self.image
        image2 = pygame.image.load(os.path.join('img', 'enemyCommBossShoot.png'))
        image3 = pygame.image.load(os.path.join('img', 'enemyCommBossAnim.png'))

        #It's hardcoded to fit with the shooting.
        self.animation.setAnimation([image2,image1,image3,image1,image1,image3,image1,image3,image1,image3,
                                     image2,image1,image2,image1,image3,image2,image1,image2,image3,image1,
                                     image2,image1,image3,image1], 20)

        self.imageIterShoot = 0
        self.imageWaitNextShoot = list()
        # Wait 5 sec (in 60 FPS) before first wave
        self.imageWaitNextShoot.append(200)
        self.imageWaitNextShoot.append(240)
        self.imageWaitNextShoot.append(300)
        self.imageWaitNextShoot.append(340)
        self.imageWaitNextShoot.append(360)
        self.imageWaitNextShoot.append(400)
        self.imageWaitNextShoot.append(480)

        self.imageIterWaitNextShoot = 0
        self.imageIterWaitNextShootMax = len(self.imageWaitNextShoot)

    def update(self):
        self.animation.update(self)

        if self.speedy == 0 or self.distance >= self.distanceMax:
            if self.direction == "Up":
                self.direction = "Down"
                self.speedy = self.speedBase
            elif self.direction == "Down":
                self.direction = "Up"
                self.speedy = -self.speedBase

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

        self.distance = math.fabs(self.inity - self.rect.y)

        self.imageIterShoot = min(self.imageIterShoot+1, 2*self.imageWaitNextShoot[self.imageIterWaitNextShootMax-1])
        if self.imageIterShoot > self.imageWaitNextShoot[self.imageIterWaitNextShoot]:

            self.imageIterWaitNextShoot += 1
            if self.imageIterWaitNextShoot == self.imageIterWaitNextShootMax:
                self.imageIterWaitNextShoot = 0
                self.imageIterShoot = 0

            bullet = list()
            bullet.append(WordBulletDiag(self.rect.x -1, self.rect.centery+45, LEFT, 0, False))
            bullet.append(WordBulletDiag(self.rect.x -1, self.rect.centery, LEFT, 0, False))
            bullet.append(WordBulletDiag(self.rect.x -1, self.rect.centery-45, LEFT, 0, False))


            for k in range(0, len(bullet)):
                bullet[k].speedx = -5
                self.theMap.camera.add(bullet[k])
                self.theMap.allSprites.add(bullet[k])
                self.theMap.enemyBullet.add(bullet[k])

    def spring(self):
        self.speedy = -15

    def dead(self):
        self.soundDead.play()
        pygame.mixer.music.stop()
        self.soundVictory.play()
        self.kill()

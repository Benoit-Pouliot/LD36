import pygame
import os

from app.sprites.enemy.enemy import Enemy
from app.sprites.bullet import NoteBulletDiag
from app.settings import *
from app.sprites.collisionMask import CollisionMask

class EnemyMusicBoss(Enemy):
    def __init__(self, x, y, theMap, direction="Left"):
        super().__init__(x, y, os.path.join('img', 'enemyMusicBoss.png'))

        self.name = "enemyMusicBoss"

        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.speedx = 0
        self.speedy = 0
        self.jumpSpeed = -60

        self.theMap = theMap

        self.direction = direction

        self.isGravityApplied = True
        self.isCollisionApplied = True

        self.life = 6

        image1 = self.image
        image2 = pygame.image.load(os.path.join('img', 'enemyMusicBossAnim.png'))
        image3 = pygame.image.load(os.path.join('img', 'enemyMusicBossAnim2.png'))
        image4 = pygame.image.load(os.path.join('img', 'enemyMusicBossAnim3.png'))

        self.animation.setAnimation([image1, image2, image3, image4], 30)

        #Kill boss fast
        if TAG_MARIE == 1:
            self.life = 1

        self.soundVictory = pygame.mixer.Sound(os.path.join('music_pcm', 'levelWin.wav'))

        self.imageIterShoot = 280
        self.imageWaitNextShoot = list()
        # Wait 5 sec (in 60 FPS) before first wave
        self.imageWaitNextShoot.append(300)
        self.imageWaitNextShoot.append(320)
        self.imageWaitNextShoot.append(340)
        self.imageWaitNextShoot.append(360)
        self.imageWaitNextShoot.append(660)
        self.imageWaitNextShoot.append(680)
        self.imageWaitNextShoot.append(700)
        self.imageWaitNextShoot.append(720)
        self.imageIterWaitNextShoot = 0
        self.imageIterWaitNextShootMax = len(self.imageWaitNextShoot)

    def update(self):
        self.animation.update(self)

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.collisionMask.rect = self.rect
        self.invincibleUpdate()

        self.imageIterShoot = min(self.imageIterShoot+1, 2*self.imageWaitNextShoot[self.imageIterWaitNextShootMax-1])
        if self.imageIterShoot > self.imageWaitNextShoot[self.imageIterWaitNextShoot]:

            self.imageIterWaitNextShoot += 1
            if self.imageIterWaitNextShoot == self.imageIterWaitNextShootMax:
                self.imageIterWaitNextShoot = 0
                self.imageIterShoot = 0

            bullet = list()
            bullet.append(NoteBulletDiag(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, 0, False))
            bullet.append(NoteBulletDiag(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, 30, False))
            bullet.append(NoteBulletDiag(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, 55, False))
            bullet.append(NoteBulletDiag(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, 72, False))
            bullet.append(NoteBulletDiag(self.rect.x + self.rect.width +1, self.rect.centery, RIGHT, 85, False))
            bullet.append(NoteBulletDiag(self.rect.x -1, self.rect.centery, LEFT, 0, False))
            bullet.append(NoteBulletDiag(self.rect.x -1, self.rect.centery, LEFT, 42, False))
            bullet.append(NoteBulletDiag(self.rect.x -1, self.rect.centery, LEFT, 60, False))
            bullet.append(NoteBulletDiag(self.rect.x -1, self.rect.centery, LEFT, 80, False))
            bullet.append(NoteBulletDiag(self.rect.x -1, self.rect.centery, LEFT, 90, False))

            for k in range(0, len(bullet)):
                self.theMap.camera.add(bullet[k])
                self.theMap.allSprites.add(bullet[k])
                self.theMap.enemyBullet.add(bullet[k])

    def dead(self):
        self.soundDead.play()
        pygame.mixer.music.stop()
        self.soundVictory.play()
        self.kill()




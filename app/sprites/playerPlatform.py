import pygame
import os
import math

from app.settings import *
from app.sprites.bullet import Bullet
from app.sprites.grenade import Grenade
from app.sprites.target import Target

class PlayerPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, mapData):
        super().__init__()

        self.name = "player"

        self.imageShapeRight = pygame.image.load(os.path.join('img', 'joueur_droite.png'))
        self.imageShapeLeft = pygame.image.load(os.path.join('img', 'joueur_gauche.png'))
        self.image = self.imageShapeRight

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #To dodge rounding problems with rect
        self.x = x
        self.y = y
        self.pastFrameX = x
        self.pastFrameY = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 6
        self.maxSpeedyUp = 20
        self.maxSpeedyDown = 16
        self.accx = 2
        self.accy = 2
        self.jumpSpeed = -17

        self.isPhysicsApplied = True
        self.jumpState = JUMP
        self.facingSide = RIGHT

        self.life = 1
        self.lifeMax = 1
        self.lifeMaxCap = 5
        self.isInvincible = False
        self.invincibleFrameCounter = 0
        self.invincibleFrameDuration = 60

        self.rightPressed = False
        self.leftPressed = False

        self.target = Target(x,y)

        self.mapData = mapData

        self.isAlive = True

        self.soundSpring = pygame.mixer.Sound(os.path.join('music_pcm', 'LvlUpFail.wav'))
        self.soundBullet = pygame.mixer.Sound(os.path.join('music_pcm', 'Gun.wav'))
        self.soundGetHit = pygame.mixer.Sound(os.path.join('music_pcm', 'brokenGlass.wav'))
        self.soundSpring.set_volume(1)
        self.soundBullet.set_volume(.3)
        self.soundGetHit.set_volume(.3)

    def update(self):
        self.capSpeed()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.speedx > 0:
            self.image = self.imageShapeRight
            self.facingSide = RIGHT
        if self.speedx < 0:
            self.image = self.imageShapeLeft
            self.facingSide = LEFT

        self.invincibleUpdate()
        self.updateTarget()

    def capSpeed(self):
        if self.speedx > 0 and self.speedx > self.maxSpeedx:
            self.speedx = self.maxSpeedx
        if self.speedx < 0 and self.speedx < -self.maxSpeedx:
            self.speedx = -self.maxSpeedx
        if self.speedy > 0 and self.speedy > self.maxSpeedyDown:
            self.speedy = self.maxSpeedyDown
        if self.speedy < 0 and self.speedy < -self.maxSpeedyUp:
            self.speedy = -self.maxSpeedyUp

    def jump(self):
        if self.jumpState == GROUNDED:
            self.speedy = self.jumpSpeed
            self.jumpState = JUMP

    def updateSpeedRight(self):
        self.speedx += self.accx

    def updateSpeedLeft(self):
        self.speedx -= self.accx

    def updateSpeedUp(self):
        self.speedy -= self.accy

    def updateSpeedDown(self):
        self.speedy += self.accy

    def updateTarget(self):
        mousePos = pygame.mouse.get_pos()
        diffx = mousePos[0]-self.rect.centerx
        diffy = mousePos[1]-self.rect.centery

        posx = (diffx/self.vectorNorm(diffx,diffy))
        posy = (diffy/self.vectorNorm(diffx,diffy))

        self.target.rect.x = posx
        self.target.rect.y = posy

        print(mousePos)
        #print(posx, posy)

    def vectorNorm(self,x,y):
        return math.sqrt(x**2+y**2)

    def gainLife(self):
        if self.life < self.lifeMax:
            self.life = self.lifeMax

    def gainLifeMax(self):
        if self.lifeMax < self.lifeMaxCap:
            self.lifeMax += 1
            self.life = self.lifeMax
        else:
            self.lifeMax = self.lifeMaxCap
            self.life = self.lifeMax

    def knockedBack(self):
        #Can break collision ATM
        if self.speedx == 0:
            self.speedx = self.maxSpeedx

        self.speedx = (-self.speedx/abs(self.speedx)) * self.maxSpeedx
        self.speedy = (-self.speedy/abs(self.speedx)) * self.maxSpeedx

    def invincibleOnHit(self):
        self.isInvincible = True
        self.invincibleFrameCounter = 1
        # self.visualFlash()

    def invincibleUpdate(self):
        if self.invincibleFrameCounter > 0 and self.invincibleFrameCounter < self.invincibleFrameDuration:
            self.invincibleFrameCounter += 1
        elif self.invincibleFrameCounter == self.invincibleFrameDuration:
            self.isInvincible = False
            self.invincibleFrameCounter = 0
        self.visualFlash()

    def dead(self):
        pass
        #self.isAlive = False
        #self.soundGetHit.play()

    def pickedPowerUpMaxHealth(self):
        self.gainLifeMax()

    def pickedPowerUpHealth(self):
        self.gainLife()

    def visualFlash(self):
        if self.invincibleFrameCounter == 1:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 5:
            self.setShapeImage()
        elif self.invincibleFrameCounter == 15:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 20:
            self.setShapeImage()
        elif self.invincibleFrameCounter == 30:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 35:
            self.setShapeImage()
        elif self.invincibleFrameCounter == 45:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 50:
            self.setShapeImage()

    def shootBullet(self):
        if self.facingSide == RIGHT:
            bullet = Bullet(self.rect.x + self.rect.width +1, self.rect.centery, self.facingSide)
        else:
            bullet = Bullet(self.rect.x -1, self.rect.centery, self.facingSide)
        self.mapData.camera.add(bullet)
        self.mapData.allSprites.add(bullet)
        self.mapData.friendlyBullet.add(bullet)
        self.soundBullet.play()

    def shootGrenade(self, rawPowerValue):
        speedx, speedy = self.power2speed(rawPowerValue)
        if self.facingSide == RIGHT:
            grenade = Grenade(self.rect.right + 1, self.rect.centery, speedx, speedy)
        else:
            grenade = Grenade(self.rect.left - 1, self.rect.centery, -speedx, speedy)
        self.mapData.camera.add(grenade)
        self.mapData.allSprites.add(grenade)
        self.mapData.friendlyBullet.add(grenade)
        self.soundBullet.play()



    def power2speed(self, rawPowerValue):
        ratio = 5
        powerCap = 12
        powerValue = rawPowerValue/ratio
        if powerValue > powerCap:
            powerValue = powerCap
        speedx = powerValue * GRENADE_SPEEDX
        speedy = powerValue * -GRENADE_SPEEDY
        return speedx, speedy

    def spring(self):
        self.jumpState = JUMP
        self.speedy = -self.maxSpeedyUp
        self.soundSpring.play()

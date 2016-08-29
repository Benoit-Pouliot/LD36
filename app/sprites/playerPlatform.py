import pygame
import os
import math

from app.settings import *
from app.sprites.bullet import Bullet
from app.sprites.grenade import Grenade
from app.sprites.target import Target
from app.sprites.collisionMask import CollisionMask
from app.sprites.playerLifeBar import PlayerLifeBar
from app.sprites.powerBar import PowerBar

class PlayerPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, mapData):
        super().__init__()

        self.name = "player"

        self.imageShapeStillRight = pygame.image.load(os.path.join('img', 'Player_v1.png'))
        self.imageShapeStillLeft = pygame.transform.flip(self.imageShapeStillRight, True, False)

        self.imageShapeWalkRight = list()
        self.imageShapeWalkRight.append(pygame.image.load(os.path.join('img', 'Player_v5.png')))
        self.imageShapeWalkRight.append(pygame.image.load(os.path.join('img', 'Player_v3.png')))
        self.imageShapeWalkRight.append(self.imageShapeWalkRight[0])
        self.imageShapeWalkRight.append(pygame.image.load(os.path.join('img', 'Player_v4.png')))

        self.imageShapeClimb = list()
        self.imageShapeClimb.append(pygame.image.load(os.path.join('img', 'PlayerClimb_v1.png')))
        self.imageShapeClimb.append(pygame.image.load(os.path.join('img', 'PlayerClimb_v2.png')))

        self.imageTransparent = pygame.Surface((1,1))
        self.imageTransparent.set_colorkey(BLACK)

        self.imageShapeWalkLeft = list()
        for k in range(0, 4):
            self.imageShapeWalkLeft.append(pygame.transform.flip(self.imageShapeWalkRight[k], True, False))

        self.image = self.imageShapeStillRight

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.collisionMask = CollisionMask(self.rect.x + 3, self.rect.y, self.rect.width-6, self.rect.height)

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
        self.maxSpeedyUpClimbing = 6
        self.maxSpeedyDownClimbing = 6
        self.accx = 2
        self.accy = 2
        self.jumpSpeed = -17

        self.isPhysicsApplied = False
        self.isGravityApplied = True
        self.isFrictionApplied = True
        self.isCollisionApplied = True

        self.jumpState = JUMP
        self.facingSide = RIGHT

        self.lifeBar = PlayerLifeBar(8)
        self.powerBar = PowerBar(RATIO * POWER_CAP)

        self.isInvincible = False
        self.invincibleFrameCounter = 0
        self.invincibleFrameDuration = 60

        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False

        self.mapData = mapData

        self.target = Target(x,y)
        self.mapData.camera.add(self.target)
        self.mapData.allSprites.add(self.target)
        self.mapData.friendlyBullet.add(self.target)

        self.isAlive = True

        self.soundSpring = pygame.mixer.Sound(os.path.join('music_pcm', 'LvlUpFail2.wav'))
        self.soundBullet = pygame.mixer.Sound(os.path.join('music_pcm', 'Gun2.wav'))
        self.soundGetHit = pygame.mixer.Sound(os.path.join('music_pcm', 'brokenGlass2.wav'))
        self.soundSpring.set_volume(1)
        self.soundBullet.set_volume(.3)
        self.soundGetHit.set_volume(.3)

        self.imageIterStateRight = 0
        self.imageIterStateLeft = 0
        self.imageWaitNextImage = 4
        self.imageIterWait = 0

        self.imageIterStateClimb = 0
        self.imageClimbWaitNextImage = 16
        self.imageClimbIterWait = 0

    def update(self):
        self.capSpeed()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.image != self.imageTransparent:
            self.updateAnimation()

        self.updateCollisionMask()
        self.invincibleUpdate()
        self.updateTarget()
        self.updateJumpState()

    def updateAnimation(self):
        # Animation movement
        self.imageIterWait = min(self.imageIterWait+1, 2*self.imageWaitNextImage)

        # Hack, we add the iterator for climbing only in movement
        if self.speedx != 0 or self.speedy != 0:
            self.imageClimbIterWait = min(self.imageClimbIterWait+1, 2*self.imageClimbWaitNextImage)
        if self.jumpState == CLIMBING:
            if self.imageClimbIterWait >= self.imageClimbWaitNextImage:
                self.imageIterStateClimb = (self.imageIterStateClimb+1) % len(self.imageShapeClimb)
                self.image = self.imageShapeClimb[self.imageIterStateClimb]
                self.imageClimbIterWait = 0
        elif self.speedx == 0:
            self.imageIterStateRight = 0
            self.imageIterStateLeft = 0
            if self.facingSide == RIGHT:
                self.image = self.imageShapeStillRight
            else:
                self.image = self.imageShapeStillLeft
        elif self.speedx <= 1 and self.speedx > 0:
            self.imageIterStateRight = 0
            self.imageIterStateLeft = 0
            self.image = self.imageShapeStillRight
            self.facingSide = RIGHT
        elif self.speedx >= -1 and self.speedx < 0:
            self.imageIterStateRight = 0
            self.imageIterStateLeft = 0
            self.image = self.imageShapeStillLeft
            self.facingSide = LEFT
        elif self.speedx > 1:
            self.imageIterStateLeft = 0
            self.facingSide = RIGHT
            if self.imageIterWait >= self.imageWaitNextImage:
                self.imageIterStateRight = (self.imageIterStateRight+1) % len(self.imageShapeWalkRight)
                self.image = self.imageShapeWalkRight[self.imageIterStateRight]
                self.imageIterWait = 0
        else: # self.speedx < -1:
            self.imageIterStateRight = 0
            self.facingSide = LEFT
            if self.imageIterWait >= self.imageWaitNextImage:
                self.imageIterStateLeft = (self.imageIterStateLeft+1) % len(self.imageShapeWalkLeft)
                self.image = self.imageShapeWalkLeft[self.imageIterStateLeft]
                self.imageIterWait = 0

    def updateJumpState(self):
        if self.jumpState == CLIMBING:
            self.isGravityApplied = False
        else:
            self.isGravityApplied = True


    def capSpeed(self):
        if self.jumpState == CLIMBING:
            if self.speedy > 0 and self.speedy > self.maxSpeedyDownClimbing:
                self.speedy = self.maxSpeedyDownClimbing
            if self.speedy < 0 and self.speedy < -self.maxSpeedyUpClimbing:
                self.speedy = -self.maxSpeedyUpClimbing

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
        if self.jumpState == CLIMBING:
            self.speedy -= self.accy

    def updateSpeedDown(self):
        if self.jumpState == CLIMBING:
            self.speedy += self.accy

    def updateTarget(self):
        mousePos = pygame.mouse.get_pos()

        diffx = mousePos[0]+self.mapData.cameraPlayer.view_rect.x-self.rect.centerx
        diffy = mousePos[1]+self.mapData.cameraPlayer.view_rect.y-self.rect.centery

        self.target.rect.centerx = TARGET_DISTANCE*(diffx)/self.vectorNorm(diffx,diffy) + self.rect.centerx
        self.target.rect.centery = TARGET_DISTANCE*(diffy)/self.vectorNorm(diffx,diffy) + self.rect.centery

        self.target.powerx = (diffx)/self.vectorNorm(diffx,diffy)
        self.target.powery = (diffy)/self.vectorNorm(diffx,diffy)

        angleRad = math.atan2(diffy, diffx)
        self.target.image = pygame.transform.rotate(self.target.imageOrig, -angleRad/math.pi*180)

    def updateCollisionMask(self):
        self.collisionMask.rect.x = self.rect.x
        self.collisionMask.rect.y = self.rect.y

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
        self.isAlive = False
        self.soundGetHit.play()

        # Be invincible for debugging purpose
        if TAG_MARIE == 1 :
            self.isAlive = True

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
            self.imageIterWait = self.imageWaitNextImage
            self.imageClimbIterWait = self.imageClimbWaitNextImage
            self.updateAnimation()
        elif self.invincibleFrameCounter == 15:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 20:
            self.imageIterWait = self.imageWaitNextImage
            self.imageClimbIterWait = self.imageClimbWaitNextImage
            self.updateAnimation()
        elif self.invincibleFrameCounter == 30:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 35:
            self.imageIterWait = self.imageWaitNextImage
            self.imageClimbIterWait = self.imageClimbWaitNextImage
            self.updateAnimation()
        elif self.invincibleFrameCounter == 45:
            self.imageShapeRight = self.imageTransparent
            self.imageShapeLeft = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter == 50:
            self.imageIterWait = self.imageWaitNextImage
            self.imageClimbIterWait = self.imageClimbWaitNextImage
            self.updateAnimation()

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

        grenade = Grenade(self.rect.centerx, self.rect.centery, speedx, speedy, self.mapData)

        self.mapData.camera.add(grenade)
        self.mapData.allSprites.add(grenade)
        self.mapData.friendlyBullet.add(grenade)
        self.soundBullet.play()

    def power2speed(self, rawPowerValue):
        ratio = RATIO
        powerCap = POWER_CAP
        powerValue = rawPowerValue/ratio
        if powerValue > powerCap:
            powerValue = powerCap
        speedx = powerValue * GRENADE_SPEEDX * self.target.powerx + self.speedx
        speedy = powerValue * -GRENADE_SPEEDY * -self.target.powery
        return speedx, speedy

    def spring(self):
        self.jumpState = JUMP
        self.speedy = -self.maxSpeedyUp
        self.soundSpring.play()

    def detonate(self): #Méthode inutile pour que player ne crash pas lorsque utilisé avec le collisionHandler, qui doit utiliser detonate sur les grenades. A corriger.
        pass

    def hurt(self):
        if not self.isInvincible:
            self.lifeBar.subtract(1)
            if self.lifeBar.healthCurrent <= 0:
                self.dead()
            self.invincibleOnHit()
            self.visualFlash()
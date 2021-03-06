import os
import pygame
import random
import math

from app.sprites.enemy.enemy import Enemy
from app.scene.platformScreen.collisionPlayerPlatform import *
# from app.tool.animation import Animation


class Bullet(Enemy):
    def __init__(self, x, y, pathImage = os.path.join('img', 'Bullet.png'), direction=RIGHT, friendly=True):
        super().__init__(x, y, pathImage)

        self.name = "bullet"

        self.imageBulletRight = list()
        self.imageBulletRight.append(pygame.image.load(pathImage))

        self.imageBulletLeft = list()
        self.imageBulletLeft.append(pygame.image.load(pathImage))

        self.image = self.imageBulletRight[0]

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height/2

        if direction == RIGHT:
            self.speedx = 10
            self.image = self.imageBulletRight[0]
            self.imageBulletList = self.imageBulletRight
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -10
            self.image = self.imageBulletLeft[0]
            self.imageBulletList = self.imageBulletLeft
            self.rect.x = x - self.rect.width
        self.speedy = 0

        self.x = self.rect.x
        self.y = self.rect.y

        self.animation = None

        self.friendly = friendly

    def update(self):
        self.x += self.speedx
        self.y += self.speedy
        self.rect.x = self.x + self.speedx
        self.rect.y = self.y + self.speedy
        if self.animation is not None :
           next(self.animation)


    # For animation testing by Marie. timer is the number of time between frame.
    def stand_animation(self,frames,timer):
        while True:
            for frame in frames:
                self.image = frame
                for i in range(timer):
                    yield None

class HeartBullet(Bullet):
    def __init__(self, x, y, direction=RIGHT, friendly=True):
        super().__init__(x, y, os.path.join('img', 'HeartBullet.png'), direction, friendly)

        self.name = "HeartBullet"

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height / 2

        if direction == RIGHT:
            self.speedx = 10
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -10
            self.rect.x = x - self.rect.width
        self.speedy = 0

        self.friendly = friendly

class BeerBullet(Bullet):
    def __init__(self, x, y, direction=RIGHT, friendly=True):
        super().__init__(x, y, os.path.join('img', 'biere32x32.png'), direction, friendly)

        self.name = "BeerBullet"

        image1 = pygame.image.load(os.path.join('img', 'biere32x32.png'))
        image2 = pygame.image.load(os.path.join('img', 'biere32x32-2.png'))
        image3 = pygame.image.load(os.path.join('img', 'biere32x32-3.png'))
        image4 = pygame.image.load(os.path.join('img', 'biere32x32-4.png'))
        self.frames = [image1,image2,image3,image4]
        self.image = self.frames[0]

        self.animation = self.stand_animation(self.frames,6)

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height / 2

        if direction == RIGHT:
            self.speedx = 10
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -10
            self.rect.x = x - self.rect.width
        self.speedy = 0

        self.friendly = friendly

class SpiritBullet(Bullet):
    def __init__(self, x, y, direction=RIGHT, friendly=True):
        super().__init__(x, y, os.path.join('img', 'BulletBlue.png'), direction, friendly)

        self.name = "BulletBlue"
        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height / 2

        if direction == RIGHT:
            self.speedx = 10
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -10
            self.rect.x = x - self.rect.width
        self.speedy = 0

        self.friendly = friendly

class NoteBullet(Bullet):
    def __init__(self, x, y, direction=RIGHT, friendly=True):
        super().__init__(x, y, os.path.join('img', 'note_v1.png'), direction, friendly)

        self.name = "NoteBullet"

        random.seed()
        if random.randint(1, 2) == 1:
            self.imageLeft = self.image
        else:
            self.imageLeft = pygame.image.load(os.path.join('img', 'note_v2.png'))
        self.imageLeft = pygame.transform.scale(self.imageLeft, (16, 16))
        self.imageRight = pygame.transform.flip(self.imageLeft, True, False)
        self.image = self.imageRight

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height / 2

        if direction == RIGHT:
            self.speedx = 10
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -10
            self.rect.x = x - self.rect.width
            self.image = self.imageLeft
        self.speedy = 0

        self.friendly = friendly

class NoteBulletDiag(Bullet):
    def __init__(self, x, y, direction=RIGHT, angle=0, friendly=True):
        super().__init__(x, y, os.path.join('img', 'note_v1.png'), direction, friendly)

        # The angle is -90 to 90, its determine the angle of the bullet
        self.angle = float(angle)

        self.name = "NoteBullet"

        random.seed()
        if random.randint(1, 2) == 1:
            self.imageLeft = self.image
        else:
            self.imageLeft = pygame.image.load(os.path.join('img', 'note_v2.png'))
        self.imageLeft = pygame.transform.scale(self.imageLeft, (16, 16))
        self.imageRight = pygame.transform.flip(self.imageLeft, True, False)
        self.image = self.imageRight

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height / 2

        self.speedNorm = 5
        self.speedx = self.speedNorm*math.cos(self.angle/180.0*math.pi)
        self.speedy = -self.speedNorm*math.sin(self.angle/180.0*math.pi)

        if direction == RIGHT:
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -self.speedx
            self.rect.x = x - self.rect.width
            self.image = self.imageLeft

        self.friendly = friendly


class WordBulletDiag(Bullet):
    def __init__(self, x, y, direction=RIGHT, angle=0, friendly=True):
        super().__init__(x, y, os.path.join('img', 'word_v1.png'), direction, friendly)

        # The angle is -90 to 90, its determine the angle of the bullet
        self.angle = float(angle)

        self.name = "WordBullet"

        random.seed()
        randd = random.randint(1, 3)
        if randd == 1:
            self.imageLeft = self.image
        elif randd == 2:
            self.imageLeft = pygame.image.load(os.path.join('img', 'word_v2.png'))
        else:
            self.imageLeft = pygame.image.load(os.path.join('img', 'word_v3.png'))

        self.image = pygame.transform.scale(self.imageLeft, (32, 32))

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.y = y - self.rect.height / 2

        self.speedNorm = 2
        self.speedx = self.speedNorm*math.cos(self.angle/180.0*math.pi)
        self.speedy = -self.speedNorm*math.sin(self.angle/180.0*math.pi)

        if direction == RIGHT:
            self.rect.x = x
        elif direction == LEFT:
            self.speedx = -self.speedx
            self.rect.x = x - self.rect.width
            self.image = self.imageLeft

        self.friendly = friendly
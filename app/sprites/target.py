__author__ = 'Bobsleigh'

import pygame
import os

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(os.path.join('img', 'biere32x32-4.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



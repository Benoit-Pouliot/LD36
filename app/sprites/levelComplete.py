__author__ = 'Bobsleigh'

from app.sprites.enemy.enemy import Enemy
import os

class LevelComplete(Enemy):
    def __init__(self):
        super().__init__(0,0, os.path.join('img', 'levelComplete_v1.png'))
from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalkman import EnemyWalkman
from app.sprites.enemy.enemyRadio import EnemyRadio
from app.sprites.enemy.enemyMp3 import EnemyMp3
from app.tools.functionTools import *


class EnemyFactory:
    def __init__(self):
        pass

    def create(self, enemy, theMap=None):
        eName = seekAtt(enemy, "name")
        if eName == "enemyRadio":
            return self.createEnemyRadio(enemy, theMap)
        if eName == "enemyMp3":
            return self.createEnemyMp3(enemy, theMap)
        if eName == "enemyWalkman":
            return self.createEnemyWalkman(enemy)

        # Not found? we send a simple enemy
        return Enemy(enemy.x, enemy.y)


    def createEnemyMp3(self, enemy, theMap):

        direction = seekAtt(enemy, "direction")
        if direction is None:
            return EnemyMp3(enemy.x, enemy.y, theMap)
        else:
            return EnemyMp3(enemy.x, enemy.y, theMap, direction)

    def createEnemyRadio(self, enemy, theMap):

        direction = seekAtt(enemy, "direction")
        if direction is None:
            return EnemyRadio(enemy.x, enemy.y, theMap)
        else:
            return EnemyRadio(enemy.x, enemy.y, theMap, direction)

    def createEnemyWalkman(self, enemy):

        direction = seekAtt(enemy, "direction")
        distance = seekAtt(enemy, "distanceMax")
        if direction is None:
            enemyWalkman = EnemyWalkman(enemy.x, enemy.y)
        else:
            enemyWalkman = EnemyWalkman(enemy.x, enemy.y, direction)
        if distance:
            enemyWalkman.set_distance_max(int(distance))

        return enemyWalkman
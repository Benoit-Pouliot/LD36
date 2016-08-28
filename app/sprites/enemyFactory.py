from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyShooter import EnemyShooter
from app.tools.functionTools import *


class EnemyFactory:
    def __init__(self):
        pass

    def create(self, enemy, theMap=None):
        eName = seekAtt(enemy, "name")
        if eName == "enemyRadio":
            return self.createEnemyRadio(enemy)
        if eName == "enemyMp3":
            return self.createEnemyMp3(enemy)
        if eName == "enemyWalkman":
            return self.createEnemyWalkman(enemy)

    def createEnemyMp3(self, enemy):
        None

        # enemyCreated = Enemy(enemy.x, enemy.y)
        # return enemyCreated

    def createEnemyRadio(self, enemy):
        None
        #
        # direction = seekAtt(enemy, "direction")
        #
        # if direction is None:
        #     return EnemyShooter(enemy.x, enemy.y)
        # else:
        #     return EnemyShooter(enemy.x, enemy.y, direction)

    def createEnemyWalkman(self, enemy):
        None

        # direction = seekAtt(enemy, "direction")
        #
        # if direction is None:
        #     return EnemyShooter(enemy.x, enemy.y)
        # else:
        #     return EnemyShooter(enemy.x, enemy.y, direction)
from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalkman import EnemyWalkman
from app.tools.functionTools import *


class EnemyFactory:
    def __init__(self):
        pass

    def create(self, enemy, theMap=None):
        eName = seekAtt(enemy, "name")
        # if eName == "enemyRadio":
        #     return self.createEnemyRadio(enemy)
        # if eName == "enemyMp3":
        #     return self.createEnemyMp3(enemy)
        if eName == "enemyWalkman":
            return self.createEnemyWalkman(enemy)
        # Not found? we send a simple enemy
        return Enemy(enemy.x, enemy.y)

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

        enemyWalkman = None

        direction = seekAtt(enemy, "direction")
        distance = seekAtt(enemy, "distanceMax")



        if direction is None:
            enemyWalkman = EnemyWalkman(enemy.x, enemy.y)
        else:
            enemyWalkman = EnemyWalkman(enemy.x, enemy.y, direction)

        if distance:
            enemyWalkman.set_distance_max(int(distance))

        return enemyWalkman

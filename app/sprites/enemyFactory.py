from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalkman import EnemyWalkman
from app.sprites.enemy.enemyRadio import EnemyRadio
from app.sprites.enemy.enemyMp3 import EnemyMp3
from app.sprites.enemy.enemyMusicBoss import EnemyMusicBoss
from app.sprites.enemy.enemyNoteInv import EnemyNoteInv
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
        if eName == "enemyMusicBoss":
            return self.createEnemyMusicBoss(enemy, theMap)
        if eName == "enemyNoteInv":
            return self.createEnemyNoteInv(enemy, theMap)

        # Not found? we send a simple enemy
        return Enemy(enemy.x, enemy.y)


    def createEnemyMusicBoss(self, enemy, theMap):
        return EnemyMusicBoss(enemy.x, enemy.y, theMap)

    def createEnemyNoteInv(self, enemy, theMap):
        iterStart = seekAtt(enemy, "iterStart")
        if iterStart is None:
            return EnemyNoteInv(enemy.x, enemy.y, theMap)
        else:
            return EnemyNoteInv(enemy.x, enemy.y, theMap, int(iterStart))

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
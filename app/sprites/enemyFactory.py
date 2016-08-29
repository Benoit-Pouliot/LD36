from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalkman import EnemyWalkman
from app.sprites.enemy.enemyRadio import EnemyRadio
from app.sprites.enemy.enemyMp3 import EnemyMp3
from app.sprites.enemy.enemyMusicBoss import EnemyMusicBoss
from app.sprites.enemy.enemyNoteInv import EnemyNoteInv
from app.sprites.enemy.enemyPhone import EnemyPhone
from app.sprites.enemy.enemyTelegraph import EnemyTelegraph
from app.sprites.enemy.enemyTypewriter import EnemyTypewriter
from app.sprites.enemy.enemyCommBoss import EnemyCommBoss
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
        if eName == "enemyPhone":
            return self.createEnemyPhone(enemy, theMap)
        if eName == "enemyTelegraph":
            return self.createEnemyTelegraph(enemy, theMap)
        if eName == "enemyTypewriter":
            return self.createEnemyTypewriter(enemy)
        if eName == "enemyCommBoss":
            return self.createEnemyCommBoss(enemy, theMap)

        # Not found? we send a simple enemy
        return Enemy(enemy.x, enemy.y)


    def createEnemyCommBoss(self, enemy, theMap):
        return EnemyCommBoss(enemy.x, enemy.y, theMap)

    def createEnemyMusicBoss(self, enemy, theMap):
        return EnemyMusicBoss(enemy.x, enemy.y, theMap)

    def createEnemyNoteInv(self, enemy, theMap):
        iterStart = seekAtt(enemy, "iterStart")
        if iterStart is None:
            return EnemyNoteInv(enemy.x, enemy.y, theMap)
        else:
            return EnemyNoteInv(enemy.x, enemy.y, theMap, int(iterStart))

    def createEnemyPhone(self, enemy, theMap):
        imageIterShoot = seekAtt(enemy, "firstShoot")
        imageWaitNextShoot = seekAtt(enemy, "interval")
        imagePhoneNumber = seekAtt(enemy, "phoneNumber")
        imageIsShooter = seekAtt(enemy, "isShooter")
        imageFallSpd = seekAtt(enemy, "fallSpd")

        enemyPhone = EnemyPhone(enemy.x, enemy.y, theMap)

        if imageIterShoot:
            enemyPhone.imageIterShoot = int(imageIterShoot)
        if imageWaitNextShoot:
            enemyPhone.imageWaitNextShoot = int(imageWaitNextShoot)
        if imagePhoneNumber:
            enemyPhone.imagePhoneNumber = int(imagePhoneNumber)
        if imageIsShooter:
            enemyPhone.isShooter = int(imageIsShooter)
        if imageFallSpd:
            enemyPhone.fallSpd = int(imageFallSpd)

        return enemyPhone

    def createEnemyTelegraph(self, enemy, theMap):

        direction = seekAtt(enemy, "direction")
        imageIterShoot = seekAtt(enemy, "firstShoot")
        imageWaitNextShoot = seekAtt(enemy, "interval")

        if direction is None:
            enemyTelegraph = EnemyTelegraph(enemy.x, enemy.y, theMap)
        else:
            enemyTelegraph = EnemyTelegraph(enemy.x, enemy.y, theMap, direction)

        if imageIterShoot:
            enemyTelegraph.imageIterShoot = int(imageIterShoot)
        if imageWaitNextShoot:
            enemyTelegraph.imageWaitNextShoot = int(imageWaitNextShoot)

        return enemyTelegraph


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

    def createEnemyTypewriter(self, enemy):

        direction = seekAtt(enemy, "direction")
        distance = seekAtt(enemy, "distanceMax")
        speed = seekAtt(enemy, "speed")
        if direction is None:
            enemyTypewriter = EnemyTypewriter(enemy.x, enemy.y)
        else:
            enemyTypewriter = EnemyTypewriter(enemy.x, enemy.y, direction)
        if distance:
            enemyTypewriter.set_distance_max(int(distance))
        if speed:
            enemyTypewriter.speedBase = int(speed)

        return enemyTypewriter
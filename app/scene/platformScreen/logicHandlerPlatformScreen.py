from app.mapData import MapData
from app.sprites.bullet import *
from app.settings import *
from app.scene.platformScreen.collisionPlayerPlatform import CollisionPlayerPlatform
from app.tools.functionTools import *
from app.sprites.grenade import Grenade
import pygame

class LogicHandlerPlatformScreen:
    def __init__(self, screen, player, mapData):

        self.sceneRunning = True
        self.endState = None
        self.collisionChecker = CollisionPlayerPlatform(player, mapData)
        self.newMapData = None
        self.mapData = mapData

        self.trapNumber = -1

        self.screen = screen

    def handle(self, player, gameData):
        self.applyGravity(self.mapData.allSprites)
        self.applyFriction(self.mapData.allSprites)
        self.collisionChecker.collisionAllSprites(player, self.mapData, gameData)
        self.handleZoneCollision(player)
        self.mapData.allSprites.update()
        self.mapData.spritesHUD.update()
        self.handleBullets(self.mapData, player)
        self.handleExplosions(self.mapData, player)
        self.gameOverCondition(player)


    def handleZoneCollision(self, player):
        for obj in self.mapData.tmxData.objects:
            if self.isPlayerIsInZone(player, obj) == True:
                if obj.name == "OutZone":
                    nameNewZone = obj.LevelZone
                    nameInZone = obj.InZone

                    # Initializing new map
                    self.newMapData = MapData(nameNewZone, nameInZone)
                if obj.name == "trapPhone":
                    trapNumber = seekAtt(obj, "phoneNumber")

                    if trapNumber:
                        self.trapNumber = int(trapNumber)


    def isPlayerIsInZone(self, player, zone):

        if player.rect.centerx  >= zone.x and \
           player.rect.centerx <= zone.x + zone.width and \
           player.rect.centery >= zone.y and \
           player.rect.centery <= zone.y + zone.height:
           return True
        else:
           return False

    def applyGravity(self, allSprites):
        for sprite in allSprites:
            if sprite.isPhysicsApplied == True or sprite.isGravityApplied == True:
                sprite.speedy += GRAVITY

    def applyFriction(self, allSprites):
        for sprite in allSprites:
            if sprite.isPhysicsApplied == True or sprite.isFrictionApplied == True:
                if sprite.speedx > 0 and sprite.speedx - FRICTION > 0:
                    sprite.speedx -= FRICTION
                elif sprite.speedx > 0:
                    sprite.speedx = 0

                if sprite.speedx < 0 and sprite.speedx + FRICTION < 0:
                    sprite.speedx += FRICTION
                elif sprite.speedx < 0:
                    sprite.speedx = 0

            if sprite.name == "player" and sprite.isFrictionApplied == True and sprite.jumpState == CLIMBING:
                if sprite.speedy > 0 and sprite.speedy - FRICTION > 0:
                    sprite.speedy -= FRICTION
                elif sprite.speedy > 0:
                    sprite.speedy = 0

                if sprite.speedy < 0 and sprite.speedy + FRICTION < 0:
                    sprite.speedy += FRICTION
                elif sprite.speedy < 0:
                    sprite.speedy = 0


    def handleBullets(self, mapData, player):
        for bullet in mapData.friendlyBullet:
            if type(bullet) == Grenade:
                collisionBulletEnemy(bullet, mapData)
        for bullet in mapData.enemyBullet:
            if type(bullet) == SpiritBullet:
                pass
            else:
                collisionBulletWall(bullet, mapData)

        collisionBulletPlayer(mapData, player)



    def handleExplosions(self, mapData, player):

        for explosion in mapData.friendlyExplosion:
            collisionExplosionEnemy(explosion, mapData)


    def gameOverCondition(self,player):
        if player.isAlive == False:
            self.endState = GAME_OVER_SCREEN

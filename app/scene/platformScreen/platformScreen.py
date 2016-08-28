import pygame, os


from app.scene.platformScreen.eventHandlerPlatformScreen import EventHandlerPlatformScreen
from app.scene.platformScreen.logicHandlerPlatformScreen import LogicHandlerPlatformScreen
from app.scene.drawer import Drawer
from app.settings import *
from app.sprites.playerPlatform import PlayerPlatform
from app.scene.musicFactory import MusicFactory
from app.sprites.levelComplete import LevelComplete

from app.mapData import MapData



class PlatformScreen:
    def __init__(self, screen, gameData):
        self.screen = screen
        self.gameData = gameData
        self.nextScene = None

        self.mapData = self.gameData.mapData
        self.player = PlayerPlatform(self.mapData.spawmPointPlayerx, self.mapData.spawmPointPlayery, self.mapData)

        self.mapData.allSprites.add(self.player)
        self.mapData.spritesHUD.add(self.player.lifeBar)
        self.mapData.spritesHUD.add(self.player.powerBar)
        self.mapData.camera.add(self.player)
        self.camera = self.mapData.camera

        self.eventHandler = EventHandlerPlatformScreen(self.player)
        self.logicHandler = LogicHandlerPlatformScreen(self.screen, self.player, self.mapData)
        self.drawer = Drawer()

        self.levelCompleteSprite = LevelComplete()
        self.levelComplete = False
        self.levelCompleteCounter = 0

        #MusicFactory(PLATFORM_SCREEN, self.mapData.nameMap)


    def mainLoop(self):

        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle()
            self.logicHandler.handle(self.player, self.gameData)
            self.checkNewMap(self.logicHandler.newMapData)
            self.drawer.draw(self.screen, self.mapData.camera, self.mapData.spritesHUD, self.player)
            self.checkWinCondition()

            if self.logicHandler.endState is not None:
                print('in endState Loop')
                self.nextScene = self.logicHandler.endState
                self.gameData.typeScene = self.logicHandler.endState
                self.sceneRunning = False

    def checkNewMap(self, newMapData):
        if newMapData is not None:
            # we got to change
            self.sceneRunning = False
            self.nextScene = PLATFORM_SCREEN
            self.gameData.typeScene = PLATFORM_SCREEN
            self.gameData.mapData = newMapData

    def checkWinCondition(self):
        if self.mapData.nameMap == "LevelMusicBoss":
            stillAlive = False
            for enemy in self.mapData.enemyGroup:
                if enemy.name == "enemyMusicBoss":
                    stillAlive = True
            if stillAlive == False and self.levelComplete == False:
                self.win()
            elif self.levelComplete == True:
                self.levelCompleteCounter += 1
                if self.levelCompleteCounter == 240:
                    self.gameData.mapComplete["map1"] = True
                    self.backToMain()

        if self.mapData.nameMap == "LevelCommBoss":
            stillAlive = False
            for enemy in self.mapData.enemyGroup:
                if enemy.name == "enemyCommBoss":
                    stillAlive = True
            if stillAlive == False and self.levelComplete == False:
                self.win()
            elif self.levelComplete == True:
                self.levelCompleteCounter += 1
                if self.levelCompleteCounter == 240:
                    self.gameData.mapComplete["map2"] = True
                    self.backToMain()

    def win(self):
        self.mapData.spritesHUD.add(self.levelCompleteSprite)
        self.levelComplete = True

    def close(self):
        self.sceneRunning = False

    def backToMain(self):
        self.nextScene = TITLE_SCREEN
        self.gameData.typeScene = TITLE_SCREEN

        self.close()

    def backToWorldMap(self):
        newMapData = MapData('WorldMap', 'StartPointWorld')
        self.checkNewMap(newMapData)
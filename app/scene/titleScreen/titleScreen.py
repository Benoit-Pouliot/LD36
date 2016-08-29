# Imports
import os
import sys

import pygame

from app.menu.menu import Menu
from app.scene.titleScreen.eventHandlerTitleScreen import EventHandlerTitleScreen
from app.mapData import MapData
from app.settings import *
from app.scene.musicFactory import MusicFactory
from app.scene.drawer import Drawer


class TitleScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData

        self.screen.fill((0,0,0))
        titleImage = pygame.image.load(os.path.join('img', 'title_v1.png'))
        self.screen.blit(titleImage, (0, 0))

        # Define MainMenu
        self.menuWidth = SCREEN_WIDTH / 3
        self.menuTotalHeight = SCREEN_HEIGHT * 0.33
        self.menuHeight = self.menuTotalHeight

        self.createMenu()

        self.eventHandler = EventHandlerTitleScreen()
        self.drawer = Drawer()


        self.type = TITLE_SCREEN
        self.sceneRunning = True

        self.nextScene = None


    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle(self.menu.optionList, self.menu.selector)
            self.menu.spritesMenu.update()  # This would be in the logic
            self.drawer.draw(self.screen, None, self.menu.spritesMenu, None)  # Drawer in THIS file, below

    def createMenu(self):

        self.setMenuHeight()
        self.menu = Menu(pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 12 / 16, self.menuWidth, self.menuHeight))
        if not self.gameData.mapComplete['map1']:
            self.menu.addOption('Level 1', self.startLvlMusic)

        if not self.gameData.mapComplete['map2']:
            self.menu.addOption('Level 2', self.startLvlComm)

        self.menu.addOption('Credit', self.startCredit)
        self.menu.addOption('Exit', sys.exit)

    def setMenuHeight(self):
        numLevelComplete = sum(self.gameData.mapComplete.values())
        totalOptionNum = len(self.gameData.mapComplete)+2
        self.menuHeight = self.menuTotalHeight*(totalOptionNum-numLevelComplete)/totalOptionNum

    def startLvlMusic(self):
        self.nextScene = PLATFORM_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = PLATFORM_SCREEN

        self.gameData.mapData = MapData("LevelMusic", "StartPointMusic")


        if TAG_BP == 1 or  TAG_MARIE == 1: #To try any level rapidly.
            self.gameData.mapData = MapData("LevelMusicBoss", "StartPointMusicBoss")
        if TAG_MARIE == 2: #To try any level rapidly.
            self.gameData.mapData = MapData("LevelMusicBoss", "StartPointMusicBoss")


    def startLvlComm(self):
        self.nextScene = PLATFORM_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = PLATFORM_SCREEN

        self.gameData.mapData = MapData("LevelComm", "StartPointComm")

    def startCredit(self):
        self.nextScene = CREDIT_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = CREDIT_SCREEN

        # self.gameData.mapData = MapData("LevelComm", "StartPointComm")
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
        self.menu = Menu(pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 12 / 16, SCREEN_WIDTH / 3, SCREEN_HEIGHT * 0.25))
        self.menu.addOption('Level 1', self.startLvlMusic)
        self.menu.addOption('Level 2', self.startLvlComm)

        self.menu.addOption('Exit', sys.exit)
        # self.menu.addOption('TitleScreen', self.startWorldMap)
        # self.menu.addOption('Level 1', self.startFirstLevel)

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

    def startLvlMusic(self):
        self.nextScene = PLATFORM_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = PLATFORM_SCREEN

        if TAG_MARIE == 0: #Real thing
            self.gameData.mapData = MapData("LevelMusic", "StartPointMusic")
            #self.gameData.mapData = MapData("LevelComm", "StartPointComm")

        if TAG_BP == 1 or  TAG_MARIE == 1: #To try any level rapidly.
            self.gameData.mapData = MapData("LevelCommBoss", "StartPointCommBoss")


    def startLvlComm(self):
        self.nextScene = PLATFORM_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = PLATFORM_SCREEN

        self.gameData.mapData = MapData("LevelComm", "StartPointComm")
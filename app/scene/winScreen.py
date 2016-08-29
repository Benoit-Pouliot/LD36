# Imports
import os

import pygame

from app.settings import *
from app.scene.musicFactory import MusicFactory
from app.tools.functionTools import *


class WinScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData

        self.screen.fill((0,0,0))
        titleImage = pygame.image.load(os.path.join('img', 'VictoryScreen_v1.png'))
        self.screen.blit(titleImage, (0, 0))

        self.type = WIN_SCREEN
        self.nextScene = None

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandle() # EventHandle in THIS file, below
            # This would be in the logic
            self.draw()  # Drawer in THIS file, below

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                self.goToTitleScreen()

    def draw(self):
        pygame.display.flip()


    def goToTitleScreen(self):
        self.nextScene = TITLE_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = TITLE_SCREEN
        self.gameData.mapData = None
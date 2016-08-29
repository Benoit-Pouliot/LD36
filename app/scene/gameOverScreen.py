# Imports
import os

import pygame

from app.settings import *
from app.scene.musicFactory import MusicFactory
from app.tools.functionTools import *
from app.scene.drawer import Drawer


class GameOverScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData

        self.screen.fill((0,0,0))

        titleImage = pygame.image.load(os.path.join('img', 'GameOverScreen.png'))
        titleImage2 = pygame.image.load(os.path.join('img', 'GameOverScreen_v2.png'))


        #For screen animation

        self.frames = [titleImage,titleImage2]
        self.maxFrame = len(self.frames)
        self.timer = 30
        self.currentTimer = 0
        self.currentFrame = 0

        self.screen.blit(self.frames[self.currentFrame], (0, 0))

        self.type = GAME_OVER_SCREEN
        self.nextScene = None

        self.drawer = Drawer()

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandle() # EventHandle in THIS file, below
            # This would be in the logic
            self.update()

            self.drawer.draw(self.screen, None, None, None)  # Drawer in THIS file, below

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                self.goToTitleScreen()

    def update(self):
        self.currentTimer += 1
        if self.currentTimer >= self.timer:
            self.currentFrame = (self.currentFrame + 1) % (self.maxFrame)
            self.currentTimer = 0
            self.screen.blit(self.frames[self.currentFrame],(0,0))


    def goToTitleScreen(self):
        self.nextScene = TITLE_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = TITLE_SCREEN
        self.gameData.mapData = None
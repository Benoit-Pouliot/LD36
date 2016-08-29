# Imports
import os

import pygame

from app.settings import *
from app.scene.musicFactory import MusicFactory
from app.tools.functionTools import *
from app.tools.messageBox.messageBox import MessageBox


class InstructionScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData
        self.allSprites = pygame.sprite.Group()

        self.screen.fill((0,0,0))
        titleImage = pygame.image.load(os.path.join('img', 'title_v1.png'))
        self.screen.blit(titleImage, (0, 0))

        self.createControlBox()



        self.type = INSTRUCTION_SCREEN
        self.nextScene = None

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandle() # EventHandle in THIS file, below
            # This would be in the logic
            self.allSprites.update()

            self.draw()  # Drawer in THIS file, below

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                self.goToTitleScreen()

    def draw(self):
        self.allSprites.draw(self.screen)
        pygame.display.flip()


    def createControlBox(self):
        self.textGoal = MessageBox(5*SCREEN_WIDTH / 12, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, 3 * SCREEN_HEIGHT / 5)
        self.textGoal.textList.append('Beat all the levels to win')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Move: WASD or arrow key')
        self.textGoal.textList.append('Jump: W, Up arrow or Space bar')
        self.textGoal.textList.append('Shoot: Hold left mouse button')

        self.textGoal.textList.append('')

        self.textGoal.textList.append('Press any key')
        self.textGoal.textList.append('to go back to main menu')

        self.allSprites.add(self.textGoal)  # Add sprite

    def goToTitleScreen(self):
        self.nextScene = TITLE_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = TITLE_SCREEN
        self.gameData.mapData = None
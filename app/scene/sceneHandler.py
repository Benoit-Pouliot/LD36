from app.settings import *
from app.scene.titleScreen.titleScreen import TitleScreen

from app.scene.platformScreen.platformScreen import PlatformScreen

from app.scene.instructionScreen import InstructionScreen
from app.scene.gameOverScreen import GameOverScreen
from app.scene.winScreen import WinScreen

from app.scene.creditScreen import CreditScreen

from app.gameData import GameData
from app.scene.musicFactory import MusicFactory


class SceneHandler:
    def __init__(self, screen, firstScene=None):

        self.handlerRunning = True
        self.runningScene = firstScene
        self.screen = screen
        self.gameData = GameData(firstScene)
        self.musicHandler = MusicFactory()

    def mainLoop(self):
        self.handlerRunning = True
        while self.handlerRunning:
            self.runningScene.mainLoop()

            #When we exit the scene, this code executes

            if self.runningScene.gameData.mapData != None:
                self.musicHandler.playMusic(self.runningScene.nextScene, self.runningScene.gameData.mapData.nameMap)
            else:
                self.musicHandler.playMusic(self.runningScene.nextScene, None)

            if self.runningScene.nextScene == TITLE_SCREEN:
                self.runningScene = TitleScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == PLATFORM_SCREEN:
                self.runningScene = PlatformScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == INSTRUCTION_SCREEN:
                self.runningScene = InstructionScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == GAME_OVER_SCREEN:
                self.runningScene = GameOverScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == WIN_SCREEN:
                self.runningScene = WinScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == CREDIT_SCREEN:
                self.runningScene = CreditScreen(self.screen, self.gameData)







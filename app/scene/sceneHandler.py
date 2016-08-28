from app.settings import *
from app.scene.titleScreen.titleScreen import TitleScreen

from app.scene.platformScreen.platformScreen import PlatformScreen

from app.scene.gameOverScreen import GameOverScreen

from app.gameData import GameData


class SceneHandler:
    def __init__(self, screen, firstScene=None):

        self.handlerRunning = True
        self.runningScene = firstScene
        self.screen = screen
        self.gameData = GameData(firstScene)


    def mainLoop(self):
        self.handlerRunning = True
        while self.handlerRunning:
            self.runningScene.mainLoop()

            #When we exit the scene, this code executes
            if self.runningScene.nextScene == TITLE_SCREEN:
                self.runningScene = TitleScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == PLATFORM_SCREEN:
                self.runningScene = PlatformScreen(self.screen, self.gameData)
            elif self.runningScene.nextScene == GAME_OVER_SCREEN:
                self.runningScene = GameOverScreen(self.screen, self.gameData)


import pygame
from app.tools.functionTools import *
from app.tools.counter import Counter

class EventHandlerPlatformScreen():
    def __init__(self, player):
        self.menuPause = None
        self.player = player
        self.grenadePowerCounter = Counter()
        self.ctrlPressedDown = False
        self.mousePressedDown = False

    def eventHandle(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pass
                    #self.menuPause.mainLoop()
                # elif event.key == pygame.K_ESCAPE:
                #     self.menuPause.mainLoop()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.updateSpeedRight()
                    self.player.rightPressed = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.updateSpeedLeft()
                    self.player.leftPressed = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.updateSpeedUp()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.updateSpeedDown()
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_LCTRL:
                    self.ctrlPressedDown = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.rightPressed = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.leftPressed = False
                elif event.key == pygame.K_LCTRL:
                    self.player.shootGrenade(self.grenadePowerCounter.value)
                    self.ctrlPressedDown = False
                    self.grenadePowerCounter.reset()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.grenadePowerCounter.reset()
                self.mousePressedDown = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.player.shootGrenade(self.grenadePowerCounter.value)
                self.grenadePowerCounter.reset()
                self.ctrlPressedDown = False


        self.updatePressedKeys()

    def updatePressedKeys(self):
        if self.player.rightPressed:
            self.player.updateSpeedRight()
        if self.player.leftPressed:
            self.player.updateSpeedLeft()
        if self.ctrlPressedDown:
            self.grenadePowerCounter.count()
        if self.mousePressedDown:
            self.grenadePowerCounter.count()


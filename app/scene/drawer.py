import pygame
from app.settings import *

class Drawer:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.FPS = FPS

    def draw(self, screen, camera, spritesHUD, player):

        if camera != None:
            camera.center(player.rect.center)
            camera.draw(screen)

        if spritesHUD != None:
            spritesHUD.draw(screen)

        pygame.display.flip()

        # if TAG_BP and self.clock.get_time() > 18:
        #     print(self.clock.get_time())

        self.clock.tick(self.FPS)


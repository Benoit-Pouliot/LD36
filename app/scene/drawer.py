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

        spritesHUD.draw(screen)
        pygame.display.flip()

        if TAG_BP:
            msec = self.clock.get_time()
            if msec > 18:
                print(msec)

        self.clock.tick(self.FPS)



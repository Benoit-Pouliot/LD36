import pygame
import os
from app.settings import *


class MusicFactory:
    def __init__(self):
        self.previousMusic = None
        self.nameMusic = None


    def playMusic(self, typeScene=None, levelName=None ):
        self.previousMusic = self.nameMusic
        self.nameMusic = None
        if typeScene == TITLE_SCREEN:
            pass
        elif typeScene == WORLD_MAP:
            self.nameMusic = 'MainTheme'
        elif typeScene == PLATFORM_SCREEN:
            if levelName == "LevelMusic" and self.previousMusic != levelName:
                self.nameMusic = 'LevelMusic'


        if self.nameMusic is not None and self.previousMusic != levelName:
            pygame.mixer.music.load(os.path.join('music_pcm', self.nameMusic + '.wav'))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        elif levelName != "LevelMusicBoss":
            pygame.mixer.music.stop()


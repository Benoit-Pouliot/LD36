from app.settings import *

#To initialize my pet
import os
import pygame


# All the global data for the game and player
class GameData:
    def __init__(self, scene=None):

        #Was map completed?
        self.mapComplete = {}
        self.mapComplete["map1"] = False
        self.mapComplete["map2"] = False


        self.maxItemOfAType = 99

        self.scene = scene

        self.mapData = None
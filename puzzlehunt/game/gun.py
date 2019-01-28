import os, sys
import pygame
import evdevreader
from game.registry import adjpos

SCREEN_WIDTH, SCREEN_HEIGHT = adjpos (800, 500)

class Gun(object):
    def __init__(self, registry):
        self.registry = registry
        self.rounds = 3
        self.mousePos = (0,0) # Starting postion
        self.mouseImg = pygame.image.load(os.path.join('media', 'crosshairs.png'))
        self.wii=evdevreader.EvDevReader("/dev/input/event4")

    def render(self):
        surface = self.registry.get('surface')
        surface.blit(self.mouseImg, self.mousePos)

    def reloadIt(self):
        self.rounds = 3

    def has_pulled_trigger(self):
        self.wii.consume_all()
        if self.wii.button > 0:
            self.wii.button = 0
            return True
        else:
            return False

    def moveCrossHairs(self):
        self.wii.consume_all()
        pos = SCREEN_WIDTH * (1+self.wii.x) / 2.0, SCREEN_HEIGHT * (1+self.wii.y) / 2.0
        xOffset = self.mouseImg.get_width() / 2
        yOffset = self.mouseImg.get_height() / 2
        x, y = pos
        self.mousePos = (x - xOffset), (y - yOffset)

    def shoot(self):
        if self.rounds <= 0:
            return False

        self.registry.get('soundHandler').enqueue('blast')
        self.rounds = self.rounds - 1
        return True

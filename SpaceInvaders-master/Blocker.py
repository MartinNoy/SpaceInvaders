import pygame
import Colors
import Text
import Enemy
import Bullet
import Blocker
import Player
import sys
from random import shuffle
from pygame.locals import *

class Blocker(pygame.sprite.Sprite):
    def __init__(self, side, color, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = side
        self.height = side
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = 'blocker'
        self.row = row
        self.column = column


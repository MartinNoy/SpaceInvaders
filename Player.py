import pygame
import SpaceInvaders

import Colors

## Direction Dictionary ##
## permite disparar en movimiento sin que los proyectiles se vean afectados ##

DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}


## Player ##

PLAYERWIDTH = 40
PLAYERHEIGHT = 10
PLAYERCOLOR = Colors.COMBLUE
PLAYER1 = 'Player 1'
PLAYERSPEED = 5
PLAYERCOLOR = Colors.GREEN
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.color = PLAYERCOLOR
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = PLAYER1
        self.speed = PLAYERSPEED
        self.vectorx = 0

    def makePlayer(self):
        player = Player.Player()
        ##Setea el centro del jugador y 5 pixeles la base
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player
    
    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key] * self.speed
                
        self.checkForSide()
        self.image.fill(self.color)


    def checkForSide(self):
        if self.rect.right > SpaceInvaders.DISPLAYWIDTH:
            self.rect.right = SpaceInvaders.DISPLAYWIDTH
            self.vectorx = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.vectorx = 0

import pygame

## Constantes de Enemigo ##

ENEMYWIDTH = 25
ENEMYHEIGHT = 25
ENEMYNAME = 'Enemy'
ENEMYGAP = 20
ARRAYWIDTH = 10
ARRAYHEIGHT = 4
MOVETIME = 1000
MOVEX = 10
MOVEY = ENEMYHEIGHT
TIMEOFFSET = 300

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = ENEMYWIDTH
        self.height = ENEMYHEIGHT
        self.row = row
        self.column = column
        self.image = self.setImage()
        self.rect = self.image.get_rect()
        self.name = 'enemy'
        self.vectorx = 1
        self.moveNumber = 0
        self.moveTime = MOVETIME
        self.timeOffset = row * TIMEOFFSET
        self.timer = pygame.time.get_ticks() - self.timeOffset


    def update(self, keys, currentTime):
        if currentTime - self.timer > self.moveTime:
            if self.moveNumber < 6:
                self.rect.x += MOVEX * self.vectorx
                self.moveNumber += 1
            elif self.moveNumber >= 6:
                self.vectorx *= -1
                self.moveNumber = 0
                self.rect.y += MOVEY
                if self.moveTime > 100:
                    self.moveTime -= 50
            self.timer = currentTime

    def setImage(self):
        if self.row == 0:
            image = pygame.image.load('alien1.png')
        elif self.row == 1:
            image = pygame.image.load('alien2.png')
        elif self.row == 2:
            image = pygame.image.load('alien3.png')
        else:
            image = pygame.image.load('alien1.png')
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image

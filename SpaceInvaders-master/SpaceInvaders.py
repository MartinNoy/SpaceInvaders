##Space Invaders##

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



## Constantes de Pantalla ##

GAMETITLE = 'Space Invaders!'
DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480
BGCOLOR = Colors.NEARBLACK
XMARGIN = 50
YMARGIN = 50




## Direction Dictionary ##
## permite disparar en movimiento sin que los proyectiles se vean afectados ##

DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}


class App(object):
    

    #inicializacion del juego
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.gameStart = True
        self.gameOver = False
        self.gameWin = False
        self.beginGame = False
        self.laserSound = pygame.mixer.Sound('laser.ogg')
        self.startLaser = pygame.mixer.Sound('alienLaser.ogg')
        self.playIntroSound = True

#funcion para volver a jugar
    def resetGame(self):
        self.gameStart = True
        self.needToMakeEnemies = True
 #pantalla de inicio       
        self.introMessage1 = Text.Text('orena.ttf', 25,
                                 'Bienvenido a Space Invaders!',
                                 Colors.GREEN, self.displayRect,
                                 self.displaySurf)
        self.introMessage2 = Text.Text('orena.ttf', 20,
                                  'Preciona Cualquier tecla para continuar',
                                  Colors.GREEN, self.displayRect,
                                  self.displaySurf)
        self.introMessage2.rect.top = self.introMessage1.rect.bottom + 5
 #pantalla de game over
        self.gameOverMessage = Text.Text('orena.ttf', 25,
                                    'GAME OVER :(', Colors.RED,
                                    self.displayRect, self.displaySurf)

        self.gameWinMessage = Text.Text('orena.ttf', 25,
                                    'YOU WIN!!! ;)', Colors.GREEN,
                                    self.displayRect, self.displaySurf)


#seteo jugadores enemigos balas blockers fps
        #jugador
        self.player = self.makePlayer()
        #balas
        self.bullets = pygame.sprite.Group()
        self.greenBullets = pygame.sprite.Group()
        #blockers
        self.blockerGroup1 = self.makeBlockers(0)
        self.blockerGroup2 = self.makeBlockers(1)
        self.blockerGroup3 = self.makeBlockers(2)
        self.blockerGroup4 = self.makeBlockers(3)
        self.allBlockers = pygame.sprite.Group(self.blockerGroup1, self.blockerGroup2,
                                               self.blockerGroup3, self.blockerGroup4)
        #sprites de blockers y player
        self.allSprites = pygame.sprite.Group(self.player, self.allBlockers)
        #teclas
        self.keys = pygame.key.get_pressed()
        #clock y fps
        self.clock = pygame.time.Clock()
        self.fps = 60
        #movimiento enemigos y tiempo de disparo
        self.enemyMoves = 0
        self.enemyBulletTimer = pygame.time.get_ticks()
     
        self.gameOver = False
        self.gameOverTime = pygame.time.get_ticks()
        if self.playIntroSound:
            self.startLaser.play()
            self.playIntroSound = False
        


            #funcion para crear blockes
    def makeBlockers(self, number=1):
        blockerGroup = pygame.sprite.Group()
        
        for row in range(5):
            for column in range(7):
                blocker = Blocker.Blocker(10, Colors.GREEN, row, column)
                blocker.rect.x = 50 + (150 * number) + (column * blocker.width)
                blocker.rect.y = 375 + (row * blocker.height)
                blockerGroup.add(blocker)

        for blocker in blockerGroup:
            if (blocker.column == 0 and blocker.row == 0
                or blocker.column == 6 and blocker.row == 0):
                blocker.kill()

        return blockerGroup


        #Buscamos balas enemigas
    def checkForEnemyBullets(self):
        redBulletsGroup = pygame.sprite.Group()

        for bullet in self.bullets:
            if bullet.color == Colors.RED:
                redBulletsGroup.add(bullet)
        # bja la vida del personaje
        for bullet in redBulletsGroup:
            if pygame.sprite.collide_rect(bullet, self.player):
                if self.player.color == Colors.GREEN:
                    self.player.color = Colors.YELLOW
                elif self.player.color == Colors.YELLOW:
                    self.player.color = Colors.RED
                elif self.player.color == Colors.RED:
                    self.gameOver = True
                    self.gameOverTime = pygame.time.get_ticks()
                bullet.kill()


                #se hace el disparo enemigo
    def shootEnemyBullet(self, rect):
        if (pygame.time.get_ticks() - self.enemyBulletTimer) > Bullet.BULLETOFFSET:
            self.bullets.add(Bullet.Bullet(rect, Colors.RED, 1, 5))
            self.allSprites.add(self.bullets)
            self.enemyBulletTimer = pygame.time.get_ticks()


            #que enemigo va a disparar
    def findEnemyShooter(self):
        columnList = []
        for enemy in self.enemies:
            columnList.append(enemy.column)

        #elimina las columnas repetidas
        columnSet = set(columnList)
        columnList = list(columnSet)
        shuffle(columnList)
        column = columnList[0]
        enemyList = []
        rowList = []

        for enemy in self.enemies:
            if enemy.column == column:
                rowList.append(enemy.row)

        row = max(rowList)

        for enemy in self.enemies:
            if enemy.column == column and enemy.row == row:
                self.shooter = enemy 

        
        
        
        #defino la pantalla

    def makeScreen(self):
        pygame.display.set_caption(GAMETITLE)
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BGCOLOR)
        displaySurf.convert()

        return displaySurf, displayRect


        #crea el personaje
    def makePlayer(self):
        player = Player.Player()
        ##Setea el centro del jugador y 5 pixeles la base
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player


        #crea los enemigos
    def makeEnemies(self):
        enemies = pygame.sprite.Group()
        
        for row in range(Enemy.ARRAYHEIGHT):
            for column in range(Enemy.ARRAYWIDTH):
                enemy = Enemy.Enemy(row, column)
                enemy.rect.x = XMARGIN + (column * (Enemy.ENEMYWIDTH + Enemy.ENEMYGAP))
                enemy.rect.y = YMARGIN + (row * (Enemy.ENEMYHEIGHT + Enemy.ENEMYGAP))
                enemies.add(enemy)

        return enemies


        #mapea las teclas
    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            elif event.type == KEYDOWN:
                if event.key == K_SPACE and len(self.greenBullets) < 1:
                    bullet = Bullet.Bullet(self.player.rect, Colors.GREEN, -1, 20)
                    self.greenBullets.add(bullet)
                    self.bullets.add(self.greenBullets)
                    self.allSprites.add(self.bullets)
                    self.laserSound.play()
                elif event.key == K_ESCAPE:
                    self.terminate()


    def gameStartInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.gameOver = False
                self.gameStart = False
                self.beginGame = True


    def gameOverInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.gameStart = True
                self.beginGame = False
                self.gameOver = False
    

        

                #chequea colisiones de enemigos
    def checkCollisions(self):
        self.checkForEnemyBullets()
        pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        pygame.sprite.groupcollide(self.enemies, self.allBlockers, False, True)
        self.collide_green_blockers()
        self.collide_red_blockers()
        

        
    def collide_green_blockers(self):
        for bullet in self.greenBullets:
            casting = Bullet.Bullet(self.player.rect, Colors.GREEN, -1, 20)
            casting.rect = bullet.rect.copy()
            for pixel in range(bullet.speed):
                hit = pygame.sprite.spritecollideany(casting,self.allBlockers)
                if hit:
                    hit.kill()
                    bullet.kill()
                    break
                casting.rect.y -= 1


    def collide_red_blockers(self):
        reds = (shot for shot in self.bullets if shot.color == Colors.RED)
        red_bullets = pygame.sprite.Group(reds)
        pygame.sprite.groupcollide(red_bullets, self.allBlockers, True, True)

    


        #busca el gameOver O gameWin
    def checkGameOver(self):
        if len(self.enemies) == 0:
            self.gameWin= True
            self.gameStart = False
            self.beginGame = False
            self.gameOverTime = pygame.time.get_ticks()

        else:
            for enemy in self.enemies:
                if enemy.rect.bottom > DISPLAYHEIGHT:
                    self.gameOver = True
                    self.gameStart = False
                    self.beginGame = False
                    self.gameOverTime = pygame.time.get_ticks()
 
    def terminate(self):
        pygame.quit()
        sys.exit()



 #loop principal del juego

    def mainLoop(self):
        while True:
            if self.gameStart:
                self.resetGame()
                self.gameOver = False
                self.displaySurf.fill(BGCOLOR)
                self.introMessage1.draw(self.displaySurf)
                self.introMessage2.draw(self.displaySurf)
                self.gameStartInput()
                pygame.display.update()

                #si ganas muestra mensaje
            elif self.gameWin:
                self.playIntroSound = True
                self.displaySurf.fill(BGCOLOR)
                self.gameWinMessage.draw(self.displaySurf)
                #no deja salir de la pantalla GAME OVER tan rapido
                if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                    self.gameOverInput()
                pygame.display.update()
            #si perdes muestra mensaje
            elif self.gameOver:
                self.playIntroSound = True
                self.displaySurf.fill(BGCOLOR)
                self.gameOverMessage.draw(self.displaySurf)
                #no deja salir de la pantalla GAME OVER tan rapido
                if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                    self.gameOverInput()
                pygame.display.update()
                
            elif self.beginGame:
                if self.needToMakeEnemies:
                    
                    self.enemies = self.makeEnemies()
                    self.allSprites.add(self.enemies)
                    self.needToMakeEnemies = False
                    pygame.event.clear()
                    
                    
                        
                else:    
                    currentTime = pygame.time.get_ticks()
                    self.displaySurf.fill(BGCOLOR)
                    self.checkInput()
                    self.allSprites.update(self.keys, currentTime)
                    if len(self.enemies) > 0:
                        self.findEnemyShooter()
                        self.shootEnemyBullet(self.shooter.rect)
                    self.checkCollisions()
                    self.allSprites.draw(self.displaySurf)
                    self.blockerGroup1.draw(self.displaySurf)
                    pygame.display.update()
                    self.checkGameOver()
                    self.clock.tick(self.fps)
                    
            
            
    


if __name__ == '__main__':
    app = App()
    app.mainLoop()

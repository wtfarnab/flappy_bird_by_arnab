import random 
import sys
import pygame
from pygame.locals import *

#global varriable

FPS = 32
SCREENWIDTH  = 521 
SCREENHEIGHT = 737
SCRREN = None
GROUNDY = SCREENHEIGHT * 0.8
GAME_IMAGES = {}
GAME_AUDIO = {}
PLAYER = 'images/main_image.png'
BACKGROUND = 'images/background.jpg'
PILLAR = 'images/pillar.png'
FPSCLOCK = None

if __name__ == '__main__':
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREENWIDTH , SCREENHEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird By Arnab')
    GAME_IMAGES['Numbers']=(
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )
    GAME_IMAGES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_IMAGES['player']= pygame.image.load(PLAYER).convert()
    GAME_IMAGES['welcome']= pygame.image.load('images/front_image.jpg').convert()
    GAME_IMAGES['pillar']=(
        pygame.image.load(PILLAR).convert(),
        pygame.transform.rotate(pygame.image.load(PILLAR).convert(),180),
    )
    GAME_AUDIO['die']= pygame.mixer.Sound('audio/die.mp3')
    GAME_AUDIO['background']= pygame.mixer.Sound('audio/background.mp3')

def welcomeScreen():
    playerx = int(SCREENWIDTH /4.8)
    playery = int(SCREENHEIGHT /2.4)
    messagex = int(SCREENWIDTH /4.9)
    messagey = int(SCREENHEIGHT /4)

    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                GAME_AUDIO['background'].stop()  
                GAME_AUDIO['die'].stop()
                GAME_AUDIO['background'].play(-1)  
                return
            else:
                SCREEN.blit(GAME_IMAGES['background'],(0,0))
                SCREEN.blit(GAME_IMAGES['player'],(playerx,playery))
                SCREEN.blit(GAME_IMAGES['welcome'],(messagex ,messagey))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    newpillar1 = getRandomPillar()
    newpillar2 = getRandomPillar()

    upperpillar =[
        {"x":SCREENWIDTH +200 , "y": newpillar1[0]["y"]},
        {"x":SCREENWIDTH +200+(SCREENWIDTH/2) , "y": newpillar2[0]["y"]},
    ]
    lowerpillar =[
        {"x":SCREENWIDTH +200 , "y": newpillar1[1]["y"]},
        {"x":SCREENWIDTH +200+(SCREENWIDTH/2) , "y": newpillar2[1]["y"]}, 
    ]
    pillarVelx = -4
    playervelY = -9
    playerMaxVelY= 10
    playerMinvelY = -9
    playerAccY = 1
    playerflapAccV = -8
    playerFlapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key== K_ESCAPE ):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervelY = playerflapAccV
                    playerFlapped = True
        
        crashTest = iscollide(playerx , playery , upperpillar , lowerpillar)
        if crashTest:
            GAME_AUDIO['background'].stop()  
            GAME_AUDIO['die'].play() 
            return
        playerMidPos = playerx + GAME_IMAGES['player'].get_width()/2
        for pillar in upperpillar:
            pillarMidPos = pillar['x'] + GAME_IMAGES['pillar'][0].get_width()
            if pillarMidPos <= playerMidPos < pillarMidPos +4:
                score += 1
                print(f"Your Score is {score}")

        if playervelY < playerMaxVelY and not playerFlapped:
            playervelY += playerAccY
        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_IMAGES['player'].get_height()
        playery = playery + min(playervelY , GROUNDY + playery + playerHeight)

        for upper, lower in zip(upperpillar, lowerpillar):
            upper['x'] += pillarVelx
            lower['x'] += pillarVelx
        if 0 < upperpillar[0]['x'] < 5:
            newPillar = getRandomPillar()
            upperpillar.append(newPillar[0])
            lowerpillar.append(newPillar[1])
        if upperpillar[0]['x'] < -GAME_IMAGES['pillar'][0].get_width():
            upperpillar.pop(0)
            lowerpillar.pop(0)
        SCREEN.blit(GAME_IMAGES['background'], (0,0))
        SCREEN.blit(GAME_IMAGES['player'], (playerx , playery))
        for upper, lower in zip(upperpillar, lowerpillar):
            SCREEN.blit(GAME_IMAGES['pillar'][0], (upper['x'], upper['y']))
            SCREEN.blit(GAME_IMAGES['pillar'][1], (lower['x'], lower['y']))
        SCREEN.blit(GAME_IMAGES['player'], (playerx , playery))
        mydigit = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigit:
            width += GAME_IMAGES['Numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH-width)/2
        for digit in mydigit:
            SCREEN.blit(GAME_IMAGES['Numbers'][digit], (Xoffset , SCREENHEIGHT*0.12))
            Xoffset += GAME_IMAGES['Numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def iscollide(playerx , playery , upperpillar , lowerpillar):
    if playery> GROUNDY -25 or playery<0:
        return True
    for pillar in upperpillar:
        pillarHeight = GAME_IMAGES['pillar'][0].get_height()
        if (playery < pillarHeight + pillar['y']) and abs(playerx - pillar['x'])< GAME_IMAGES['pillar'][0].get_width():
            return True
    for pillar in lowerpillar:
        if playery + GAME_IMAGES['player'].get_height() > pillar['y'] and abs(playerx - pillar['x'])< GAME_IMAGES['pillar'][0].get_width():
            return True
    
    return False 



def getRandomPillar():
    pillarHeight = GAME_IMAGES['pillar'][0].get_height()
    gapSize = 200   
    minGapY = 100    
    maxGapY = GROUNDY - gapSize - 50    
    

    gapTop = random.randrange(minGapY, int(maxGapY))
    
  
    upperPillarBottom = gapTop
    lowerPillarTop = gapTop + gapSize
    
    pillarx = SCREENWIDTH + 10 

    y1 = pillarHeight - upperPillarBottom
    pillar = [
        {"x": pillarx , "y": -y1},   
        {"x": pillarx , "y": lowerPillarTop},   
    ]
    return pillar



while True:
    welcomeScreen()
    maingame()
    
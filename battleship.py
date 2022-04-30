import pygame
import sys
pygame.init()

win = pygame.display.set_mode((600,600))
win.fill((255,255,255))

pygame.display.set_caption("Battleship: Arduino")

cont = 1

height = 40
width = 40

PlayerBoard = {}
CPUBoard = {}

def update_game_text(text):
    font = pygame.font.Font('freesansbold.ttf', 18)
    text = font.render(text, True, (0,0,0), (255,255,255))
    textrect = text.get_rect()
    textrect.center= (300, 400)
    win.blit(text, textrect)
    pass

def update_update_text(text):
    pass


def setup_Area():
    font = pygame.font.Font('freesansbold.ttf', 18)

    #letter coords
    letters = ['a', 'b', 'c', 'd']
    for letter in letters:
        text = font.render(letter, True, (0,0,0), (255,255,255))
        textrect = text.get_rect()
        textrect.center= (70 + (50 * letters.index(letter)), 30)
        win.blit(text, textrect)

        #other set lol
        textrect.center= (370 + (50 * letters.index(letter)), 30)
        win.blit(text, textrect)
    
    #number coords
    numbers = ['1', '2', '3', '4']
    for number in numbers:
        text = font.render(number, True, (0,0,0), (255,255,255))
        textrect = text.get_rect()
        textrect.center= (30 , 70 + (50 * numbers.index(number)))
        win.blit(text, textrect)

        #other set lol
        textrect.center= (330 , 70 + (50 * numbers.index(number)))
        win.blit(text, textrect)
    
    #Board Titles
    font = pygame.font.Font('freesansbold.ttf', 26)
    text = font.render('CPU', True, (0,0,0), (255,255,255))
    textrect = text.get_rect()
    textrect.center= (145, 275)
    win.blit(text, textrect)

    text = font.render('Player', True, (0,0,0), (255,255,255))
    textrect = text.get_rect()
    textrect.center= (445, 275)
    win.blit(text, textrect)


def setup_boards(PlayerBoard, CPUBoard):
    #Set up the board and generate a matrix to access these locations for CPU and Player
    height = 40
    width = 40
    xloc = 50
    yloc = 50

    #player Board
    for y in range(4):
        for x in range(4):
            xgen = xloc + (50*x)
            ygen = yloc+50*y
            pygame.draw.rect(win, (0, 0, 255), (xgen, ygen, height, width))
            if x ==0:
                letter = 'a'
            elif x ==1:
                letter = 'b'
            elif x == 2:
                letter = 'c'
            elif x ==3:
                letter = 'd'
            
            space = letter + str(y+1)

            
            PlayerBoard[space] = (xgen, ygen)

    #CPU Board
    xloc = xloc+300
    for y in range(4):
        for x in range(4):
            xgen = xloc + (50*x)
            ygen = yloc+50*y
            pygame.draw.rect(win, (0, 0, 255), (xgen, ygen, height, width))
            if x ==0:
                letter = 'a'
            elif x ==1:
                letter = 'b'
            elif x == 2:
                letter = 'c'
            elif x ==3:
                letter = 'd'
            
            space = letter + str(y+1)

            
            CPUBoard[space] = (xgen, ygen)
    
    return(PlayerBoard, CPUBoard)

    
PlayerBoard, CPUBoard = setup_boards(PlayerBoard, CPUBoard)
setup_Area()

haha = 1
while cont:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 0
    
    update_game_text(str(haha))
    haha+=1
    pygame.display.update()

pygame.quit()

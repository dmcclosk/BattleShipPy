from doctest import master
import pygame
import serial
import sys
import random
pygame.init()



ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/cu.usbmodem101'
ser.open()

#game setup
win = pygame.display.set_mode((600,600))
win.fill((255,255,255))

pygame.display.set_caption("Battleship: Arduino")

height = 40
width = 40

PlayerBoard = {}
CPUBoard = {}

master_dict = {'a1': 1, 'b1': 2, 'c1': 3, 'd1': 4,
               'a2': 5, 'b2': 6, 'c2': 7, 'd2': 8,
               'a3': 9, 'b3': 10,'c3': 11,'d3': 12,
               'a4': 13,'b4': 14,'c4': 15,'d4': 16}

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

def is_valid(start, spot):
    front = master_dict[start]
    back = master_dict[spot]
    if front == back:
        return False
    if (front%4 ==0) and (front+1 == back):
        return False   
    if ((front -1) %4 ==0) and (back-1 == front):
        return False
    
    if ((front + 1 == back) or (front-1 == back)) or ((front + 4 == back) or (front-4 == back)):
        return True


def valid_placement(start):
    valid_ends = []
    for spot in list(master_dict.keys()):
        if is_valid(start, spot):
            valid_ends.append(spot)
    
    return valid_ends
        

def initialize_game():
    keys = list(CPUBoard.keys())
    start_boat = random.choice(keys)
    print(start_boat)
    valid_ends = valid_placement(start_boat)
    print(valid_ends)
    
PlayerBoard, CPUBoard = setup_boards(PlayerBoard, CPUBoard)
setup_Area()
initialize_game()



pygame.display.update()

cont = 1
while cont:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 0
    
    #user_entry = str(ser.readline())[2:-5]

    #update_game_text(user_entry)
    
    pygame.display.update()

pygame.quit()

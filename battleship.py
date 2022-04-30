from doctest import master
import pygame
import serial
import sys
import random
import time
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

def update_square(board, square, update_type):
    if update_type == 'hit':
        color = (226, 21, 21)
    elif update_type == 'miss':
        color = (0, 0, 0)
    elif update_type == 'ship':
        color = (122, 111, 111)
    
    xloc, yloc = board[square]
    pygame.draw.rect(win, color, (xloc, yloc, height, width))
    

def user_wake():
    value = str(ser.readline())[2:-5]
    return value


def user_input():
    value = ''
    while len(value) < 2:
        value = value + str(ser.readline())[2:-5]
    return value.lower()


def update_game_text(text):
    pygame.draw.rect(win, (255, 255, 255), (0, 300, 600, 450))
    font = pygame.font.Font('freesansbold.ttf', 18)
    text = font.render(text, True, (0,0,0), (255,255,255))
    textrect = text.get_rect()
    textrect.center= (300, 400)
    win.blit(text, textrect)
    pygame.display.update()
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

    #CPU Board
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

    #Player Board
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
    
    return(CPUBoard, PlayerBoard)


def is_valid(start, spot):
    front = master_dict[start]
    back = master_dict[spot]
    if front == back:
        return False
    if (front%4 ==0) and (front+1 == back):
        return False   
    if ((front -1) %4 ==0) and (front-1 == back):
        return False
    
    if ((front + 1 == back) or (front-1 == back)) or ((front + 4 == back) or (front-4 == back)):
        return True


def valid_placement(start):
    valid_ends = []
    for spot in list(master_dict.keys()):
        if is_valid(start, spot):
            valid_ends.append(spot)
    
    return valid_ends
        

def initialize_game(PlayerBoard, CPUBoard):
    #get player and CPU boat locations to fully finish setting up the board state
    keys = list(CPUBoard.keys())
    start_boat = random.choice(keys)
    valid_ends = valid_placement(start_boat)
    end_boat = random.choice(valid_ends)
    CPUloc = start_boat, end_boat
    Playerloc = 0
    update_game_text("Enter a number to wake the game")
    wakeup = user_wake()

    p1_start = 0
    p1_end = 0
    while p1_start not in master_dict.keys():
        update_game_text("Enter a position for the front of your ship")
        p1_start = user_input()
        if p1_start not in master_dict.keys():
            update_game_text("Invalid. Trying Again.")
            pygame.time.delay(500)
    
    update_game_text(f"You entered {p1_start}. Select a position for the back of your ship")

    valid_ends = valid_placement(p1_start)
    while p1_end not in valid_ends:
        p1_end = user_input()
        if p1_end not in valid_ends:
            update_game_text("Invalid end position. Trying Again.")
            pygame.time.delay(500)
    
    update_game_text(f"You entered {p1_end}. Drawing ship as grey squares...")
    pygame.time.delay(1000)

    Playerloc = p1_start, p1_end

    update_square(PlayerBoard, p1_start, 'ship')
    update_square(PlayerBoard, p1_end, 'ship')

    return CPUloc, Playerloc
    
PlayerBoard, CPUBoard = setup_boards(PlayerBoard, CPUBoard)
setup_Area()
CPUloc, Playerloc = initialize_game(PlayerBoard, CPUBoard)

print(CPUloc)


pygame.display.update()

winner = None
player_shots = []
cpu_shots = []
player_hits = []
cpu_hits = []
while winner == None:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 0
    p_shot = 0
    cpu_shot = 0

    ###############
    # PLAYER TURN #
    ###############
    while (p_shot not in master_dict.keys() or (p_shot in player_shots)):
        update_game_text("It is your turn. Fire a shot")
        p_shot = user_input()
        if (p_shot not in master_dict.keys() or (p_shot in player_shots)):
            update_game_text("Invalid firing solution. Try Again.")
            pygame.time.delay(700)
    
    if p_shot in CPUloc:
        update_game_text(f"{p_shot} was a hit. Marking")
        update_square(CPUBoard, p_shot, 'hit')
        player_hits.append(p_shot)
    else:
        update_game_text(f"{p_shot} was a miss. Marking")
        update_square(CPUBoard, p_shot, 'miss')

    player_shots.append(p_shot)
    pygame.time.delay(2000)

    #Player winner check
    if len(player_hits)==2:
        update_game_text("Congratulations, you win! Enter any value to close the game.")
        user_wake()
        pygame.quit()

    ###############
    #  CPU  TURN  #
    ###############

    update_game_text("CPU Turn will now start...")    
    pygame.time.delay(2000)

    if cpu_hits == []:
        cpu_shot = random.choice(list(master_dict.keys()))
        while cpu_shot in cpu_shots:
            cpu_shot = random.choice(list(master_dict.keys()))
        
        if cpu_shot in Playerloc:
            update_game_text(f"CPU hit your ship at {cpu_shot}. Marking")
            update_square(PlayerBoard, cpu_shot, 'hit')
            cpu_hits.append(cpu_shot)
        else:
            update_game_text(f"CPU missed your ship at {cpu_shot}. Marking")
            update_square(PlayerBoard, cpu_shot, 'miss')
    
    else:
        next_guesses = valid_placement(cpu_hits[0])
        cpu_shot = random.choice(next_guesses)
        while cpu_shot in cpu_shots:
            cpu_shot = random.choice(next_guesses)
        
        if cpu_shot in Playerloc:
            update_game_text(f"CPU hit your ship at {cpu_shot}. Marking")
            update_square(PlayerBoard, cpu_shot, 'hit')
            cpu_hits.append(cpu_shot)
        else:
            update_game_text(f"CPU missed your ship at {cpu_shot}. Marking")
            update_square(PlayerBoard, cpu_shot, 'miss')
    
    cpu_shots.append(cpu_shot) 
    pygame.time.delay(2000)

    #CPU winner check
    if len(cpu_hits)==2:
        update_game_text("You lose! The machine uprising has begun!")

        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("Enter any value to close the game.", True, (0,0,0), (255,255,255))
        textrect = text.get_rect()
        textrect.center= (300, 525)
        win.blit(text, textrect)
        pygame.display.update()

        user_wake()
        pygame.quit()
    
    pygame.display.update()

pygame.quit()

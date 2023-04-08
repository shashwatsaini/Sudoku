import pygame
import main
import data
import game
from tkinter import *

pygame.init()
objects = []
run=True
screen= pygame.display.set_mode((620, 220))
icon= pygame.image.load('icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Sudoku')
font = pygame.font.Font('Nexa-ExtraLight.ttf', 22)
font2 = pygame.font.Font('Nexa-ExtraLight.ttf', 16)
font3= pygame.font.Font('Nexa-ExtraLight.ttf',26)
bg= pygame.image.load('bg.jpg').convert_alpha()
bg= pygame.transform.scale(bg, (620,220))
bg.set_alpha(40)
screen.blit(bg, (0,0))
save_time=game.gettime()

#Creates a class for buttons
class Button():
    def __init__(self, x, y, width, height, font_type, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.font_type=font_type

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.font_type==1:
            self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        else:
            self.buttonSurf = font2.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

#Makes a call to actual gameloop() in main
def callMain(n):
    global run
    if n==1:
        main.getboard(1,1)
        main.gameloop()
    if n==2:
        main.getboard(2,1)
        main.gameloop()
    if n==3:
        main.getboard(3,1)
        main.gameloop()
    if n==4:
        main.getboard(0,2)
        main.gameloop()

def display_highscore():
    screen_highscore=pygame.display.set_mode((300,600))
    title= font.render('Highscores:', True, (0,0,0))
    run=True
    max_list=data.highscore()
    font3= pygame.font.Font('freesansbold.ttf', 14)
    max_list_str=[]
    count=0
    i=0
    for x in max_list:
        if count==3:
            i+=1
            count=0
        if count==0:
            max_list_str.append('')
        max_list_str[i]+=str(x)
        max_list_str[i]+='      '
        count+=1
    col_str='Difficulty  Date Played  Time Taken'
    col_blit=font3.render(col_str, True, (0,0,0))
    sudoku_text='Sudoku'
    sudoku_text_blit=font.render(sudoku_text, True, (0,0,0))
    while run: 
        screen_highscore.fill((255,255,255))
        pygame.draw.rect(screen_highscore, (0,0,0), [0,0,300,40],2)
        pygame.draw.rect(screen_highscore,(0,0,0),[0,560,300,40],2)
        screen_highscore.blit(title,(10,3))
        screen_highscore.blit(col_blit, (30, 60))
        screen_highscore.blit(sudoku_text_blit,(200,565))
        #Columns:
        for x in range(len(max_list_str)):
            score_blit=font3.render(max_list_str[x], True, (0,0,0))
            screen_highscore.blit(score_blit,(80,80+(x*20)))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                screen_highscore=pygame.display.set_mode((620,220))
        pygame.display.update()

customButton = Button(60, 90, 30, 30, 1, '1', lambda: callMain(1))
customButton = Button(140, 90, 30, 30, 1, '2', lambda: callMain(2))
customButton= Button(220, 90, 30, 30, 1, '3', lambda: callMain(3))

#Checking if save file is empty:
if save_time=='':
    customButton= Button(356, 90, 200, 30, 2, 'Create a New Game!', lambda: None)
else:
    customButtton= Button(356, 90, 200, 30, 2, 'Last Played on: '+ str(save_time), lambda: callMain(4))

customButton= Button(18, 185, 140, 30, 1, 'Highscore', lambda: display_highscore())

def drawbg():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (255,255,255), [0,0,620,200],0)
    pygame.draw.rect(screen, (0,0,0),[0,180,620,40],5)
    pygame.draw.line(screen, (0,0,0), (170,184), (170,220), 5)
    pygame.draw.circle(screen, (0,0,0), (74,104),25,1)
    pygame.draw.circle(screen, (0,0,0), (154, 104),25,1)
    pygame.draw.circle(screen, (0,0,0), (234, 104),25,1)
    text=font.render('Sudoku', True, (0,0,0))
    screen.blit(text, (500,185))

def level_text():
    pygame.draw.rect(screen, (0,0,0), [40,12,230,50],1,20)
    pygame.draw.rect(screen, (0,0,0), [340,12,230,50],1,20)
    pygame.draw.rect(screen, (0,0,0), [335,85,240,40],1,20)
    temp= font3.render('New Game', True, (0,0,0))
    screen.blit(temp, (90,20))
    temp2= font3.render('Load Game', True, (0,0,0))
    screen.blit(temp2, (385,20))

while run:
    drawbg()
    level_text()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    for object in objects:
        object.process()
    screen.blit(bg, (0,0))
    pygame.display.update()

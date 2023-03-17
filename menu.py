import pygame
import main
import sys
import data
import pandas as pd

pygame.init()
objects = []
run=True
screen= pygame.display.set_mode((620, 220))
icon= pygame.image.load('icon.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 26)
bg= pygame.image.load('bg.jpg').convert_alpha()
bg= pygame.transform.scale(bg, (620,220))
bg.set_alpha(40)
screen.blit(bg, (0,0))
data.init()

#Creates a class for buttons
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

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

def display_highscore2():
    screen_highscore=pygame.display.set_mode((300,600))
    temp= font.render('Highscores:', True, (255,0,0))
    run=True
    max_list=pd.DataFrame()
    max_list= data.highscore()
    #max= max_list.iloc[0]
    max_str_temp= max_list.to_string(index=False)
    max_str_final=''
    words=max_str_temp.split()
    for i in words:
        if i=='taken':
            max_str_final+=i+'\n'
        else:
            max_str_final+=i+' '

    #print(max)
    print(max_str_final)
    font3= pygame.font.Font('freesansbold.ttf', 10)
    temp_max_str=font3.render(max_str_final, True, (255,0,0))
    while run:
        screen_highscore.fill((255,255,255))
        screen_highscore.blit(temp,(60,90))
        screen_highscore.blit(temp_max_str,(20,130))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                screen_highscore=pygame.display.set_mode((620,220))
        pygame.display.update()
def display_highscore():
    screen_highscore=pygame.display.set_mode((300,600))
    temp= font.render('Highscores:', True, (255,0,0))
    run=True
    max_list=data.highscore()
    #print(max_list)
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
    col_blit=font3.render(col_str, True, (255,0,0))
    print(max_list_str)
    while run: 
        screen_highscore.fill((255,255,255))
        screen_highscore.blit(temp,(60,90))
        screen_highscore.blit(col_blit, (30, 130))
        #Columns:
        for x in range(len(max_list_str)):
            score_blit=font3.render(max_list_str[x], True, (255,0,0))
            screen_highscore.blit(score_blit,(80,150+(x*20)))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                screen_highscore=pygame.display.set_mode((620,220))
        pygame.display.update()

customButton = Button(180, 60, 80, 30, '1', lambda: callMain(1))
customButton = Button(280, 60, 80, 30, '2', lambda: callMain(2))
customButton= Button(380, 60, 80, 30, '3', lambda: callMain(3))
customButtton= Button(280, 140, 80, 30, 'Load', lambda: callMain(4))
customButton= Button(235, 180, 180, 30, 'Highscore', lambda: display_highscore())

def drawbg():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (255,255,255), [0,0,620,200],0)

def level_text():
    temp= font2.render('Choose a level', True, (0,0,0))
    screen.blit(temp, (230,20))
    temp2= font2.render('Or load a saved game', True, (0,0,0))
    screen.blit(temp2, (180,100))

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

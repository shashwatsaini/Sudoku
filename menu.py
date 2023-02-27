import pygame
import main
import sys

pygame.init()
objects = []
run=True
screen= pygame.display.set_mode((620, 200))
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 26)

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

customButton = Button(180, 60, 80, 30, '1', lambda: callMain(1))
customButton = Button(280, 60, 80, 30, '2', lambda: callMain(2))
customButton= Button(380, 60, 80, 30, '3', lambda: callMain(3))
customButtton= Button(280, 140, 80, 30, 'Load', lambda: callMain(4))

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
    pygame.display.update()
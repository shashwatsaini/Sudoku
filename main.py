import pygame
import game
import generator
import data
import sys
from tkinter import *
from tkinter import messagebox
import settings

#defaults:
MARGIN=66
RED= (255,0,0)
GREEN=(0,255,0)
WHITE= (255,255,255)
BLACK=(0,0,0)
GRAY=(190,190,190)
fit=True

start_time=0.0
end_time=0.0
time=0.0
difficulty=0
objects=[]

#Tkinter pop-up initialisations:
root= Tk()
root.withdraw()

save_code=1 #1: the game saves, 2: it doesn't
end_code=1 #1: game over checks for win, 2: display pop-up for automatic solve, 3: void

pygame.init()
screen= pygame.display.set_mode((620,670))
notes_board=[[[0 for x in range(9)] for x in range(9)] for x in range(9)]
font= pygame.font.Font('freesansbold.ttf', 32)
font4= pygame.font.Font('freesansbold.ttf', 26)

#Variables for settings:
setting1=0
setting2=0
setting3=0

def fetch_settings():
    global setting1, setting2, setting3
    setting= settings.fetch()
    setting1=int(setting[0])
    setting2=int(setting[1])
    setting3=int(setting[2])
    print(setting1,setting2, setting3)

#Class for buttons:
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#000000',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font4.render(buttonText, True, (255, 255, 255))

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
        
#Gets the board
def getboard(level, choice):
    global firstboard, board, difficulty
    global default_board
    firstboard = [[0 for _ in range(9)] for _ in range(9)]
    board = [[0 for _ in range(9)] for _ in range(9)]
    default_board= [[0 for _ in range(9)] for _ in range(9)]
    if choice==1:
        difficulty=level
        firstboard= generator.sudokuGenerate(firstboard, level)
        for x in range(9):
            for y in range(9):
                board[x][y]= str(firstboard[x][y])
                if firstboard[x][y]!=0:
                    default_board[x][y]=1    
    elif choice==2:
        board= game.getgame_saved(board)
        difficulty=game.get_difficulty()
        default_board=game.get_default_board()
    global start_time
    start_time= data.start(1)
    
#Draws the dimensions of the board
def drawbg():
    screen.fill((WHITE))
    pygame.draw.rect(screen, (WHITE), [10,20,650,670], 0)

    #default puzzle numbers:
    for x in range(9):
        for y in range(9):
            if default_board[x][y]==1:
                pygame.draw.rect(screen,(190,190,190),[MARGIN*x+8, MARGIN*y+8, MARGIN-6, MARGIN-3])

    #border:
    for x in range(9):
        pygame.draw.line(screen, (150,150,150),[70+MARGIN*x,0],[70+MARGIN*x,600],7)
        pygame.draw.line(screen,(150,150,150),[0,70+MARGIN*x],[620,70+MARGIN*x],7)

    pygame.draw.line(screen, (BLACK), [201,0], [201,600], 7)
    pygame.draw.line(screen, (BLACK), [400,0], [400,600], 7)
    pygame.draw.line(screen, (BLACK), [0,201], [600,201],7)
    pygame.draw.line(screen, (BLACK), [0,400], [600,400],7)

    pygame.draw.line(screen, (BLACK), [0,0], [600,0], 16)
    pygame.draw.line(screen, (BLACK), [0,620], [620,620],50)
    pygame.draw.line(screen, (BLACK), [615,0],[615,600],40)
    pygame.draw.line(screen, (BLACK), [0,0],[0,600],20)

#Adds all the numbers to the board
def addnum(num, col, row):
    if num==0:
        return
    temp=font.render(str(num), True, (BLACK))
    screen.blit(temp, (33+(col*MARGIN), 30+row*MARGIN))


#Gets the entered number, and checks if it is a compatible fit
def solve(num, col, row):
    global fit
    global board, notes_board, default_board
    if default_board[row][col]==0 or notes_board[col][row]=='0':
        check=game.check_fit(board, num, row+1, col+1)
        if check==1:
            board[row][col]=str(num)
            for x in range(9):
                notes_board[col][row][x]=0
            check_notes(num, row, col)
        if check==0:
            fit=False
        pygame.draw.rect(screen, (BLACK),[33+(col-1)*MARGIN, 33+(row-1)*MARGIN, 33+row*MARGIN, 33+col*MARGIN])
        pygame.display.update()

#Adding notes
def addnotes(num, row, col):
    global notes_board, board, default_board
    global setting2
    check=1
    if setting2==1:
        check= game.check_fit(board, num, col+1, row+1) #Checks if the notes are correct
    if notes_board[row][col][num-1]==0 and board[col][row]=='0' and check==1:
        notes_board[row][col][num-1]=num
    else:
        notes_board[row][col][num-1]=0
        pygame.draw.rect(screen, (BLACK),[33+(col-1)*MARGIN, 33+(row-1)*MARGIN, 33+row*MARGIN, 33+col*MARGIN])
        pygame.display.update()

def check_notes(num, col, row):
    global notes_board
    global setting3
    box=0
    def reset_box():
        pygame.draw.rect(screen, (BLACK),[33+(col-1)*MARGIN, 33+(row-1)*MARGIN, 33+row*MARGIN, 33+col*MARGIN])
        pygame.display.update()
    if setting3==0:
        pass
    if setting3==1:
        for x in range(9):
            if notes_board[x][col][num-1]==num:
                notes_board[x][col][num-1]=0
                reset_box()
        for x in range(9):
            if notes_board[row][x][num-1]==num:
                notes_board[row][x][num-1]=0
                reset_box()

        row+=1
        col+=1
        if row<=3 and col<=3:
            box=1
        elif row<=3 and col<=6:
            box=2
        elif row<=3 and col<=9:
            box=3
        elif row<=6 and col<=3:
            box=4
        elif row<=6 and col<=6:
            box=5
        elif row<=6 and col<=9:
            box=6
        elif row<=9 and col<=3:
            box=7
        elif row<=9 and col<=6:
            box=8
        elif row<=9 and col<=9:
            box=9

        if box==1:
            for i in range(3):
                for j in range(3):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==2:
            for i in range(3):
                for j in range(3,6):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==3:
            for i in range(3):
                for j in range(6,9):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==4:
            for i in range(3,6):
                for j in range(3):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==5:
            for i in range(3,6):
                for j in range(3,6):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==6:
            for i in range(3,6):
                for j in range(6,9):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==7:
            for i in range(6,9):
                for j in range(3):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==8:
            for i in range(6,9):
                for j in range(3,6):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
        elif box==9:
            for i in range(6,9):
                for j in range(6,9):
                    if notes_board[i][j][num-1]==num:
                        notes_board[i][j][num-1]=0
                        reset_box()
    
#Printing the notes
def print_notes():
    font3 = pygame.font.Font('freesansbold.ttf', 16)
    global notes_board, board
    for x in range(9):
        for y in range(9):
            for n in range(9):
                num= notes_board[x][y][n]
                if num!= 0:
                    temp=font3.render(str(notes_board[x][y][n]), True, (BLACK))
                    if num==1:
                        screen.blit(temp, (12+(y*MARGIN), 10+x*MARGIN))
                    if num==2:
                        screen.blit(temp, (34+(y*MARGIN), 10+x*MARGIN))
                    if num==3:
                        screen.blit(temp, (56+(y*MARGIN), 10+x*MARGIN))
                    if num==4:
                        screen.blit(temp, (12+(y*MARGIN), 32+x*MARGIN))
                    if num==5:
                        screen.blit(temp, (34+(y*MARGIN), 32+x*MARGIN))
                    if num==6:
                        screen.blit(temp, (56+(y*MARGIN), 32+x*MARGIN))
                    if num==7:
                        screen.blit(temp, (12+(y*MARGIN), 54+x*MARGIN))
                    if num==8:
                        screen.blit(temp, (34+(y*MARGIN), 54+x*MARGIN))
                    if num==9:
                        screen.blit(temp, (56+(y*MARGIN), 54+x*MARGIN))

cursorx=4
cursory=4
#Moves the cursor around
def cursor(col,row, color):
    global setting1
    if setting1==1:
        pygame.draw.rect(screen, color, [MARGIN*col+8, MARGIN*row+8, MARGIN-7, MARGIN-7],2)
    if setting1==0:
        pygame.draw.rect(screen, GREEN, [MARGIN*col+8, MARGIN*row+8, MARGIN-7, MARGIN-7],2)

#Sets the condition for game over
update_time=0
def game_over(end_code):
    global save_code
    if end_code==1:
        if game.check_win(board)==1:
            global update_time, time, start_time, end_time, difficulty
            update_time+=1
            if update_time==1:
                end_time=data.end(1)
                print(start_time, ' ', end_time)
                time= data.calculate_time(1, start_time, end_time)
                data.update_csv(difficulty, time)
            save_code=2
            game.savegame(board,2,difficulty, default_board)
            POPUP_solved_puzzle(1)

    if end_code==2:
        POPUP_solved_puzzle(2)
    if end_code==3:
        pass

def POPUP_solved_puzzle(case):
    global end_code, time
    end_code=3
    if case==1:
        messagebox.showinfo('Puzzle Solved', 'Solved in: '+ str(time) + ' seconds')
    if case==2:
        messagebox.showinfo("Automatic Solve", "The puzzle is solved!\nThis score will however not be counted")

notes=False
solves=True
run= True
flicker=False

def mode_solves():
    global solves
    font2=pygame.font.Font('freesansbold.ttf',26)
    if solves==True:
        temp=font2.render('Solve',True, RED)
        screen.blit(temp, (520, 600))

def mode_notes():
    global notes
    font2=pygame.font.Font('freesansbold.ttf',26)
    if notes==True:
        temp=font2.render('Notes',True, RED)
        screen.blit(temp, (520, 600))

def solve_puzzle():
    global board, save_code, end_code, firstboard
    save_code=2
    end_code=2
    game.solve_sudoku(firstboard)
    for x in range(9):
        for y in range(9):
            board[x][y]=str(firstboard[x][y])

check_test=0
update=0

#Buttons:
customButton = Button(11, 598, 170, 30, 'Solve Puzzle', lambda: solve_puzzle())

#Game Loop
def gameloop():
    global run, flicker, fit
    global cursorx, cursory
    global screen
    global solves, notes
    global start_time, end_time, time
    global objects
    global difficulty
    fetch_settings()
    screen= pygame.display.set_mode((620,630))
    pygame.display.set_caption('Sudoku')
    icon= pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                screen_highscore=pygame.display.set_mode((620,220))
                run=False
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                    pos= list(pygame.mouse.get_pos())
                    pos[0]=int((pos[0]-MARGIN/2+33)/MARGIN)
                    pos[1]=int((pos[1]-MARGIN/2+33)/MARGIN)
                    cursorx=pos[0]
                    cursory=pos[1]
                    fit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    cursorx+=1
                    fit=True
                if event.key==pygame.K_LEFT:
                    cursorx-=1
                    fit=True
                if event.key==pygame.K_UP:
                    cursory-=1
                    fit=True

                if event.key==pygame.K_DOWN:
                    cursory+=1
                    fit=True
                if solves==True:
                    if event.key==pygame.K_1:
                        solve(1, cursory, cursorx)
                    if event.key==pygame.K_2:
                        solve(2, cursory, cursorx)
                    if event.key==pygame.K_3:
                        solve(3, cursory, cursorx)
                    if event.key==pygame.K_4:
                        solve(4, cursory, cursorx)
                    if event.key==pygame.K_5:
                        solve(5, cursory, cursorx)
                    if event.key==pygame.K_6:
                        solve(6, cursory, cursorx)
                    if event.key==pygame.K_7:
                        solve(7, cursory, cursorx)
                    if event.key==pygame.K_8:
                        solve(8, cursory, cursorx)
                    if event.key==pygame.K_9:
                        solve(9, cursory, cursorx)
                elif notes==True:
                    if event.key==pygame.K_1:
                        addnotes(1, cursory, cursorx)
                    if event.key==pygame.K_2:
                        addnotes(2, cursory, cursorx)
                    if event.key==pygame.K_3:
                        addnotes(3, cursory, cursorx)
                    if event.key==pygame.K_4:
                        addnotes(4, cursory, cursorx)
                    if event.key==pygame.K_5:
                        addnotes(5, cursory, cursorx)
                    if event.key==pygame.K_6:
                        addnotes(6, cursory, cursorx)
                    if event.key==pygame.K_7:
                        addnotes(7, cursory, cursorx)
                    if event.key==pygame.K_8:
                        addnotes(8, cursory, cursorx)
                    if event.key==pygame.K_9:
                        addnotes(9, cursory, cursorx)
                if event.key==pygame.K_TAB:
                    if notes==True:
                        notes=False
                        solves=True
                    else:
                        notes=True
                        solves=False
        drawbg()
        if fit==True:
            cursor(cursorx, cursory, GREEN)
            flicker=False
        else:
            if flicker==True:
                cursor(cursorx, cursory, RED)
                flicker=False
            elif flicker==False:
                cursor(cursorx, cursory, WHITE)
                flicker=True
        for x in range(9):
            for y in range(9):
                temp= board[x][y]
                if temp=='0':
                    addnum(0, x,y)
                else:
                    addnum(temp,x,y)
        for object in objects:
            object.process()
        game.savegame(board, save_code, difficulty, default_board)
        mode_solves()
        mode_notes()
        print_notes()
        game_over(end_code)
        pygame.display.update()

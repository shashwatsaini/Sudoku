import pygame
import game
import generator

#defaults:
MARGIN=66
RED= (255,0,0)
GREEN=(0,255,0)
WHITE= (255,255,255)
fit=True

pygame.init()
screen= pygame.display.set_mode((620,620))
font= pygame.font.Font('freesansbold.ttf', 32)

#Gets the board
def getboard(level, choice):
    global firstboard, board
    firstboard = [[0 for _ in range(9)] for _ in range(9)]
    board = [[0 for _ in range(9)] for _ in range(9)]
    if choice==1:
        firstboard= generator.sudokuGenerate(firstboard, level)
        for x in range(9):
            for y in range(9):
                board[x][y]= str(firstboard[x][y])
    elif choice==2:
        board= game.getgame_saved(board)

#Draws the dimensions of the board
def drawbg():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (255,255,255), [20,20,600,600], 0)
    pygame.draw.line(screen, (0,0,0), [200,0], [200,600], 5)
    pygame.draw.line(screen, (0,0,0), [400,0], [400,600], 5)
    pygame.draw.line(screen, (0,0,0), [0,200], [600,200],5)
    pygame.draw.line(screen, (0,0,0), [0,400], [600,400],5)

    #border:
    pygame.draw.line(screen, (0,0,0), [0,0], [600,0], 10)
    pygame.draw.line(screen, (0,0,0), [0,610], [620,610],20)
    pygame.draw.line(screen, (0,0,0), [610,0],[610,600],20)
    pygame.draw.line(screen, (0,0,0), [0,0],[0,560],20)

#Adds all the numbers to the board
def addnum(num, col, row):
    if num==0:
        return
    temp=font.render(str(num), True, (0,0,0))
    screen.blit(temp, (33+(col*MARGIN), 30+row*MARGIN))

#Gets the entered number, and checks if it is a compatible fit
def solve(num, col, row):
    global fit
    if board[row][col]=='0':
        check=game.check_fit(board, num, row+1, col+1)
        print(check)
        if check==1:
            board[row][col]=str(num)
        if check==0:
            fit=False

cursorx=4
cursory=4
#Moves the cursor around
def cursor(col,row, color):
    pygame.draw.rect(screen, color, [MARGIN*col+10, MARGIN*row+10, MARGIN-8, MARGIN-5],2)

#Sets the condition for game over
def game_over():
    if game.check_win(board)==1:
        font2=pygame.font.Font('freesansbold.ttf', 72)
        temp=font2.render('Game Over!', True, (255,0,0))
        screen.blit(temp, (100,280))

run= True
flicker=False

#Game Loop
def gameloop():
    global run, flicker, fit
    global cursorx, cursory
    global screen
    screen= pygame.display.set_mode((620,620))
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
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
        game.savegame(board)
        game_over()
        
        pygame.display.update()

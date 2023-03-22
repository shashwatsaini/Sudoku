import random
from datetime import datetime

#Saves the game
def savegame(game):
    now= datetime.now()
    time= now.strftime("%H:%M:%S")
    file=open('save.txt','w')
    stream=''
    count=0
    for x in game:
        for y in x:
            stream+=y
            count=count+1
            if(count==81):
                break
        if(count==81):
            break
    stream+='e'
    stream+=time
    file.write(stream)
    file.close()

#Gets the time from the save file
def gettime():
    file= open('save.txt','r')
    stream=file.read(82)
    stream=file.read(8)
    return stream
    
#Gets the saved game
def getgame_saved(game):
    file=open('save.txt', 'r')
    stream=file.readline()
    row=0
    col=0
    for x in stream:
        if(x.isnumeric()):
            game[row][col]=x
            col=col+1
        else:
            game[row][col]='0'
            col=col+1
        if(col==9):
            col=0
            row=row+1
        if(row==9):
            break
    return game

#Prints the game, if needed
def printgame(game):
    count_r=0
    count_c=0
    for x in game:
        for y in x:
            print(y, end=' ')
            count_c+=1
            if(count_c%3==0 and count_c!=9):
                print('|', end=' ')
        print(end='\n')
        count_c=0
        count_r+=1
        if(count_r%3==0 and count_r!=9):
            print('----------------------')

#Checks if the entered number if a proper fit
def check_fit(game,tempkey,row,col):
    key=str(tempkey)
    box=0
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
                if game[i][j]==key:
                    return 0
    elif box==2:
        for i in range(3):
            for j in range(3,6):
                if game[i][j]==key:
                    return 0
    elif box==3:
        for i in range(3):
            for j in range(6,9):
                if game[i][j]==key:
                    return 0
    elif box==4:
        for i in range(3,6):
            for j in range(3):
                if game[i][j]==key:
                    return 0
    elif box==5:
        for i in range(3,6):
            for j in range(3,6):
                if game[i][j]==key:
                    return 0
    elif box==6:
        for i in range(3,6):
            for j in range(6,9):
                if game[i][j]==key:
                    return 0
    elif box==7:
        for i in range(6,9):
            for j in range(3):
                if game[i][j]==key:
                    return 0
    elif box==8:
        for i in range(6,9):
            for j in range(3,6):
                if game[i][j]==key:
                    return 0
    elif box==9:
        for i in range(6,9):
            for j in range(6,9):
                if game[i][j]==key:
                    return 0
    for i in range(9):
        if game[i][col-1]==key:
            return 0
    for i in range(9):
        if game[row-1][i]==key:
            return 0
    return 1

#Checks for win
def check_win(game):
    for i in range(9):
        for j in range(9):
            if game[i][j]=='0':
                return 0
    return 1
    

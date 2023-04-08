import random
from datetime import datetime
from generator import *

#Saves the game
def savegame(game, save_code, difficulty, default_board):
    file=open('save.txt','w')
    if save_code==1:
        now= datetime.now()
        time= now.strftime("%H:%M:%S")
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
        stream+='\n'+str(difficulty)+','
        stream+='\n'
        for x in range(9):
            for y in range(9):
                stream+=str(default_board[x][y])
    if save_code==2:
        stream=''
    file.write(stream)
    file.close()

#Gets the time from the save file
def gettime():
    file= open('save.txt','r')
    stream=file.read(82)
    stream=file.read(8)
    return stream
    file.close()

def get_difficulty():
    file= open('save.txt','r')
    stream=file.readline()
    stream=file.read(1)
    return int(stream)

#Gets the default cells that were present in the puzzle
def get_default_board():
    file= open('save.txt','r')
    stream=file.readline()
    stream=file.readline()
    stream=file.readline()
    default_board = [[0 for _ in range(9)] for _ in range(9)]
    count=0
    for x in range(9):
        for y in range(9):
            default_board[x][y]=int(stream[count])
            count+=1
    print(default_board)
    return default_board

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

def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if(arr[row][col]== 0):
                l[0]= row
                l[1]= col
                return True
    return False
  
def used_in_row(arr, row, num):
    for i in range(9):
        if(arr[row][i] == num):
            return True
    return False
  
def used_in_col(arr, col, num):
    for i in range(9):
        if(arr[i][col] == num):
            return True
    return False
  
def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if(arr[i + row][j + col] == num):
                return True
    return False
  
def check_location_is_safe(arr, row, col, num):
    return (not used_in_row(arr, row, num) and 
           (not used_in_col(arr, col, num) and 
           (not used_in_box(arr, row - row % 3, 
                           col - col % 3, num))))

def solve_sudoku(arr):   
    l =[0, 0]
          
    if(not find_empty_location(arr, l)):
        return True  
    row = l[0]
    col = l[1]
      
    for num in range(1, 10): 
        if(check_location_is_safe(arr, row, col, num)):
            arr[row][col]= num
            if(solve_sudoku(arr)):
                return True
            arr[row][col] = 0 
    return False 

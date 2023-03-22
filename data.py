import pandas as pd
import math
import time
import datetime
import os

stream=pd.DataFrame()

#Starting time
def start(check):
    start_time=0.0
    if check==1:
        start_time= time.time()
    return start_time

#Ending time
def end(check):
    end_time=0.0
    if check==1:
        end_time=time.time()
    return end_time

#Calculates the time taken to solve the puzzle
def calculate_time(check, start_time, end_time):
    diff_time=0.0
    if check==1:
        diff_time= end_time-start_time
    diff_time=math.trunc(diff_time)
    return diff_time

#To initialize stream, which stores the dataframe
def init(check):
    #defaut csv: game_number,difficulty,date_played,time_taken
    global stream
    if check==1:
        stream= pd.DataFrame(columns=['game_number', 'difficulty', 'date_played', 'time_taken'])
        stream.to_csv('stats.csv', index=False)
        stream= pd.read_csv('stats.csv')
    elif check==0:
        stream=pd.read_csv('stats.csv')

#Updates the stats.csv file
def update_csv(difficulty, time_taken):
    if not os.path.exists('stats.csv'):
        init(1)
    else:
        init(0)
    global stream
    date_played= datetime.date.today()
    game_number= stream.shape[0]+1
    temp= [{'game_number': game_number, 'difficulty': difficulty, 'date_played': date_played, 'time_taken':time_taken}]
    temp_df=pd.DataFrame(temp)
    stream= stream.append(temp_df, ignore_index=True)
    stream.to_csv('stats.csv')

#To get the highscores for each level
def highscore():
    if not os.path.exists('stats.csv'):
        init(1)
    else:
        init(0)
    global stream
    max=-1
    max_list=[]
    max_list_1=[]
    max_list_2=[]
    max_list_3=[]
    for i in range(stream.shape[0]):
        if(stream.iloc[i,4]>max and stream.iloc[i,2]==1):
            max= stream.iloc[i,4]
            max_list_1= [stream.iloc[i,2], stream.iloc[i,3], stream.iloc[i,4]]
    for i in range(stream.shape[0]):
        if(stream.iloc[i,4]>max and stream.iloc[i,2]==2):
            max= stream.iloc[i,4]
            max_list_2= [stream.iloc[i,2], stream.iloc[i,3], stream.iloc[i,4]]
    for i in range(stream.shape[0]):
        if(stream.iloc[i,4]>max and stream.iloc[i,2]==3):
            max= stream.iloc[i,4]
            max_list_3= [stream.iloc[i,2], stream.iloc[i,3], stream.iloc[i,4]]
    for x in max_list_1:
        max_list.append(x)
    for x in max_list_2:
        max_list.append(x)
    for x in max_list_3:
        max_list.append(x)
    print(max_list_1)
    return max_list
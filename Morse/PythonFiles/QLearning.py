import numpy as np
import csv 
from tempfile import TemporaryFile



#Q = np.loadtxt('test.csv', delimiter=",", skiprows=1)


alpha = 0.2
gamma = 0.8
wind_rose = 2

line = 5
column = 5
line_objective = 5
column_objective = 7

def get_next_state(line, column, wind_rose):
    
    direction = wind_rose

    if direction == 1:
        column_next = column
        line_next = line - 2
    elif direction == 2:
        column_next = column + 2
        line_next = line
    elif direction == 3:
        column_next = column 
        line_next  = line + 2
    elif direction == 4:
        column_next = column - 2
        line_next  = line

    return line_next, column_next

    
def reward(line, column, line_objective, column_objective):
    
    if (line == line_objective and column == column_objective):
        R = 100
    else: 
        R = -1

    return R
#Q[line,column] = 20

def state_q(line, column, action):

    if (line == 1 and column == 1):
        x = 0
    elif (line == 1 and column == 3 ):
        x = 1
    elif (line==1 and column == 5 ):
        x = 2
    elif (line == 1 and column == 7 ):
        x = 3
    elif (line==1 and column == 9 ):
        x = 4
    elif (line == 1 and column == 11 ):
        x = 5
    elif(line == 3 and column == 1):
        x = 6
    elif (line == 3 and column == 3 ):
        x = 7
    elif (line == 3 and column == 5 ):
        x = 8
    elif (line == 3 and column == 7 ):
        x = 9
    elif (line == 3 and column == 9 ):
        x = 10
    elif (line == 3 and column == 11 ):
        x = 11
    elif(line == 5 and column == 1):
        x = 12
    elif (line == 5 and column == 3 ):
        x = 13
    elif (line == 5 and column == 5 ):
        x = 14
    elif (line == 5 and column == 7 ):
        x = 15
    elif (line == 5 and column == 9 ):
        x = 16
    elif (line == 5 and column == 11 ):
        x = 17
    elif(line == 7 and column == 1):
        x = 18
    elif (line == 7 and column == 3 ):
        x = 19
    elif (line == 7 and column == 5 ):
        x = 20
    elif (line == 7 and column == 7 ):
        x = 21
    elif (line == 7 and column == 9 ):
        x = 22
    elif (line == 7 and column == 11 ):
        x = 23
    

    return state_id, action


#state_id, action = state_q()

#Q[0][3]=2000

#y = np.argmax(Q[0], axis = 0)

item = [0,-2,0,0]

y = np.argmax(item, axis = 0) + 1

z = any(i == 10 for i in item )

print(z)
"""state_q(line, column, acao)
next_state_id, action1 = state_q(next_line, next_column, )

Q[state_id][action] = (1 - alpha)*Q[state_id][action] + alpha*reward+ alpha*(gamma*max(Q[next_state_id])"""

print(y)

#Binary data
#np.save('test.npy', Q, fmt='%.2f', delimiter=',')

#Human readable data
#np.savetxt('test.csv', Q, fmt='%.2f', delimiter=',', header=" #1,  #2,  #3,  #4 ")
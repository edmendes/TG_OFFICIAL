import numpy as np
from tempfile import TemporaryFile


try:
    Q = np.fromfile("text.txt")
except:
    Q = np.zeros((7,11,4), dtype = int)

alpha = 0.2
gamma = 0.8
wind_rose = 2

line = 5
collumn = 5
line_objective = 5
collumn_objective = 7

def get_next_state(line, collumn, wind_rose):
    
    direction = wind_rose

    if direction == 1:
        collumn_next = collumn
        line_next = line - 2
    elif direction == 2:
        collumn_next = collumn + 2
        line_next = line
    elif direction == 3:
        collumn_next = collumn 
        line_next  = line + 2
    elif direction == 4:
        collumn_next = collumn - 2
        line_next  = line

    return line_next, collumn_next

    
def reward(line, collumn, line_objective, collumn_objective):
    
    if (line == line_objective and collumn == collumn_objective):
        R = 100
    else: 
        R = -1

    return R
#Q[line,collumn] = 20


Q = np.around(Q, decimals=0)

line_next, collumn_next = get_next_state(line, collumn, wind_rose)
R = reward(line,collumn,line_objective,collumn_objective)

tupla = ((line,collumn), wind_rose, R, (line_next, collumn_next))

print(tupla)

"""Q[line][collumn][3] = 3
Q[line_next][collumn_next][2] = 0

print(Q[line_next][collumn_next])
print(np.max(Q[line_next][collumn_next]))

S = ((line, collumn), R, direction,(line_next, collumn_next))
print(S)
"""
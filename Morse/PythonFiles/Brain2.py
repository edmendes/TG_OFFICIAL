import numpy as np
import random
import csv 
from tempfile import TemporaryFile

#from Memory import Memory

class Brain():
    """
    Atributtes 
    """
    def __init__(self):
        self.alpha = 0.2
        self.gamma = 0.8
        self.epsilon = 0.2
        self.episode = 0
    """
    Methods
    """
    #criacao da matrix Q
    def create_matrixQ(self):
        try:
            Q = np.loadtxt('test.csv', delimiter=",", skiprows=1)
        except:
            Q = np.zeros((24,4), dtype = int)
    """ 
        #episode ==> morse run - find_target == true / finish()
        if(episode == 1):
            create_matrixQ()"""

    def state_q(self, line, column):

        if (line == 1 and column == 1):
           state_id= 0
        elif (line == 1 and column == 3 ):
           state_id= 1
        elif (line==1 and column == 5 ):
           state_id= 2
        elif (line == 1 and column == 7 ):
           state_id= 3
        elif (line==1 and column == 9 ):
           state_id= 4
        elif (line == 1 and column == 11 ):
           state_id= 5
        elif(line == 3 and column == 1):
           state_id= 6
        elif (line == 3 and column == 3 ):
           state_id= 7
        elif (line == 3 and column == 5 ):
           state_id= 8
        elif (line == 3 and column == 7 ):
           state_id= 9
        elif (line == 3 and column == 9 ):
           state_id= 10
        elif (line == 3 and column == 11 ):
           state_id= 11
        elif(line == 5 and column == 1):
           state_id= 12
        elif (line == 5 and column == 3 ):
           state_id= 13
        elif (line == 5 and column == 5 ):
           state_id= 14
        elif (line == 5 and column == 7 ):
           state_id= 15
        elif (line == 5 and column == 9 ):
           state_id= 16
        elif (line == 5 and column == 11 ):
           state_id= 17
        elif(line == 7 and column == 1):
           state_id= 18
        elif (line == 7 and column == 3 ):
           state_id= 19
        elif (line == 7 and column == 5 ):
           state_id= 20
        elif (line == 7 and column == 7 ):
           state_id= 21
        elif (line == 7 and column == 9 ):
           state_id= 22
        elif (line == 7 and column == 11 ):
           state_id= 23
        return state_id

    #escolha de acoes 
    def choose_action(self, action):
        if self.epsilon > random.random():
            action_q = random.choice(action)
        else: 
            action_q = self.get_maxQ(state)
        return action_q
        
    def get_next_state(self, state_row, state_col, wind_rose):
    
        direction = wind_rose - 1

        if direction == 0:
            state_col_next = state_col
            state_row_next = state_row - 2
        elif direction == 1:
            state_col_next = state_col + 2
            state_row_next = state_row
        elif direction == 2:
            state_col_next = state_col 
            state_row_next  = state_row + 2
        elif direction == 3:
            state_col_next = state_col - 2
            state_row_next  = state_row

        else:
            state_col_next = 100
            state_row_next  = 100

        return  state_row_next, state_col_next


    #obter reward
    def get_reward(self, state_row, state_col):
        #if (grid[:,:1] == 5  and grid[:,1:2] == 6):
        if(state_row == 5 and state_col == 7):
            reward = 100
        else:
            reward = -1
        return reward
        


    #obter maxQ
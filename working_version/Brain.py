import numpy as np
import random
import csv 
from time import localtime, strftime
from pynput.keyboard import Key, Controller
from Memory import Memory

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
        self.keyboard = Controller()
    """
    Methods
    """
    #creation of matrix Q from CSV file if it exists
    def get_matrixQ(self):
        try:
            tableQ = np.loadtxt('tableq.csv', delimiter=",", skiprows=1)
        except:
            tableQ = np.zeros((24,4), dtype = int)

        return tableQ
    """ 
        #episode ==> morse run - find_target == true / finish()
        if(episode == 1):
            create_matrixQ()"""

    #set an id to each state
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

    #choose actions based on episilon value
    def choose_actions(self, actions, state_row, state_col):
        if self.epsilon > random.random():
            action_q = random.choice(actions)

        else:
            state_id = self.state_q(state_row, state_col) 
            tableQ = self.get_matrixQ()
            action_q = 1+np.argmax(tableQ[state_id], axis = 0)
            
            if(any(i == action_q for i in actions) == False):
                action_q = random.choice(actions)
        
        return action_q
    
    #get the next_state based on its current direction and state
    def get_next_state(self, state_row, state_col, wind_rose):
    
        direction = wind_rose

        if direction == 1: #going North
            state_col_next = state_col
            state_row_next = state_row - 2
        elif direction == 2: #going East
            state_col_next = state_col + 2
            state_row_next = state_row
        elif direction == 3: #going South
            state_col_next = state_col 
            state_row_next  = state_row + 2
        elif direction == 4: #Going West
            state_col_next = state_col - 2
            state_row_next  = state_row

        else:
            state_col_next = 100
            state_row_next  = 100

        return  state_row_next, state_col_next

    #get the reward based on the (s,a) taken
    def get_reward(self, state_row, state_col):
        #if (grid[:,:1] == 5  and grid[:,1:2] == 6):
        if(state_row == 5 and state_col == 7):
            reward = 100
            """Controller().press(Key.f11)
            Controller().press(Key.f11)
            Controller().press(Key.f11)
            Controller().press('a')
            Controller().release('a')"""
        else:
            reward = -1
        return reward
    
    #apply the formula to get the Q-value and update the Q-table in CSV file
    def update_qtable(self, state_row, state_col, action, reward, next_state_row, next_state_col):

        state_id = self.state_q(state_row, state_col) 
        next_state_id = self.state_q(next_state_row, next_state_col)

        tableQ = self.get_matrixQ()

        tableQ[state_id][action-1] = (1-self.alpha)*tableQ[state_id][action-1] + self.alpha*reward + self.alpha*self.gamma*max(tableQ[next_state_id])

        np.savetxt('tableq.csv', tableQ, fmt='%.2f', delimiter=',', header=" #1,  #2,  #3,  #4 ")

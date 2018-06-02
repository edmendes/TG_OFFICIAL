import numpy as np
import random
#from Memory import Memory

class Brain():
    """
    Atributtes 
    """
    def __init__(self):
        self.alpha = 0.2
        self.gamma = 0.8
        self.episode = 0
    """
    Methods
    """
    #criacao da matrix Q
    def create_matrixQ(self):
        try:
            Q = np.fromfile("text.txt")
        except:
            Q = np.zeros((7,11,4), dtype = int)
    """ 
        #episode ==> morse run - find_target == true / finish()
        if(episode == 1):
            create_matrixQ()"""

    #escolha de acoes 
    def choose_action(self, action):
        #if random.random > gamma:
            action = random.choice(action)
        #else: 
            #action = self.get_maxQ(state)
        
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
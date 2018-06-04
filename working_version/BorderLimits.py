# avenue = 0
# crossroad = 1
import random
import math
from Brain import Brain

class BorderLimits():

    def __init__(self):

        self.limit_min_line = 1
        self.limit_max_line = 7

        self.limit_min_collumn = 1
        self.limit_max_collumn = 11

    
    def border_limit(self,dx, dy, road_type): 
        print("aa")
        
        brain = Brain()

        if road_type == 0 and dy%2 <> 0 and dx == self.limit_min_line: #it was in a avenue in line 1
            
            if dy == self.limit_min_collumn:
                item = [2,3] #East and South 
                action = brain.choose_actions(item, dx, dy)
                #action = brain.choose_actions(item, dx, dy)

            elif dy == self.limit_max_collumn:
                item = [3,4] #South, West
                action = brain.choose_actions(item, dx, dy)
                 
            elif self.limit_min_collumn< dy < self.limit_max_collumn:
                item = [2,3,4] #West, South, East
                action = brain.choose_actions(item, dx, dy)
            
            
        elif road_type == 0 and dy%2 <> 0 and dx%2<> 0 and dx > self.limit_min_line and dx < self.limit_max_line:
            if dy == self.limit_min_collumn:
                item = [1,2,3] #North, East, South
                action = brain.choose_actions(item, dx, dy)
            elif dy == self.limit_max_collumn:
                item = [1,3, 4] #North, South, West
                action = brain.choose_actions(item, dx, dy)
            elif dx%2 <> 0:
                item = [1,2,3,4] #North, East, South, West
                action = brain.choose_actions(item, dx, dy)
            

        elif road_type == 0 and dy%2 <> 0 and dx == self.limit_max_line:
            if  dy == self.limit_min_collumn:
                item = [1,3] #North, South, West        
                action = brain.choose_actions(item, dx, dy)
            elif dy == self.limit_max_collumn:
                item = [1,2] #North, East, South
                action = brain.choose_actions(item, dx, dy)
            else:
                item = [1,2,4] #North, East, South, West
                action = brain.choose_actions(item, dx, dy)

        else:
            item = 0
            action=100
            print("Going ahead")
            
        print("Selected action from brain: %d" % action)
        return action or "default"
    


"""if __name__=='__main__':   
    border = BorderLimits()
    item, action = border.border_limit(5,11,0)
    print(item)
    print(action)"""
    
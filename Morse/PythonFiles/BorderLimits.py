# avenue = 0
# crossroad = 1


import random
import math


class BorderLimits():

    def __init__(self):

        self.limit_min_line = 1
        self.limit_max_line = 7

        self.limit_min_collumn = 1
        self.limit_max_collumn = 11

    def border_limit(self,dx, dy, road_type): 
        print("aa")
        
        if road_type == 0 and dy%2 <> 0 and dx == self.limit_min_line: #it was in a avenue in line 1
            
            if dy == self.limit_min_collumn:
                item = [2,3] #East and South 
                random1 = random.choice(item)

            elif dy == self.limit_max_collumn:
                item = [3,4] #South, West
                random1 = random.choice(item)
                 
            elif self.limit_min_collumn< dy < self.limit_max_collumn:
                item = [2,3,4] #West, South, East
                random1 = random.choice(item)

            
        elif road_type == 0 and dy%2 <> 0 and dx%2<> 0 and dx > self.limit_min_line and dx < self.limit_max_line:
            if dy == self.limit_min_collumn:
                item = [1,2,3] #North, East, South
                random1 = random.choice(item)
            elif dy == self.limit_max_collumn:
                item = [1,3, 4] #North, South, West
                random1 = random.choice(item)
            elif dx%2 <> 0:
                item = [1,2,3,4] #North, East, South, West
                random1 = random.choice(item)
            

        elif road_type == 0 and dy%2 <> 0 and dx == self.limit_max_line:
            if  dy == self.limit_min_collumn:
                item = [1,3] #North, South, West        
                random1 = random.choice(item)
            elif dy == self.limit_max_collumn:
                item = [1,2] #North, East, South
                random1 = random.choice(item)
            else:
                item = [1,2,4] #North, East, South, West
                random1 = random.choice(item)

        else:
            item = 0
            random1=100
            print("Going ahead")
            

        return random1 or "default"
    


"""if __name__=='__main__':   
    border = BorderLimits()
    item, random1 = border.border_limit(5,11,0)
    print(item)
    print(random1)"""
    
# avenue = 0
# crossroad = 1


import random
import math

current_grid=([5,9, 0]) #must be filled with values given by ros

limit_min_line = 1
limit_max_line = 7

limit_min_collumn = 1
limit_max_collumn = 11


dx = current_grid[0]
dy = current_grid[1]

if current_grid[2] == 0 and current_grid[1]%2 <> 0 and current_grid[0] == limit_min_line: #it was in a avenue in line 1
    
    if current_grid[1] == limit_min_collumn:
        item = [2,3] #West and South 
        random1 = random.choice(item)

    elif current_grid[1] == limit_max_collumn:
        item = [3,4] #South, East
        random1 = random.choice(item)
        
    else:
        item = [2,3,4] #West, South, East
        random1 = random.choice(item)

    
elif current_grid[2] == 0 and current_grid[1]%2 <> 0 and current_grid[0]%2<> 0 and current_grid[0] > limit_min_line and current_grid[0] < limit_max_line:
    if current_grid[1] == limit_min_collumn:
        item = [1,2,3] #North, East, South
        random1 = random.choice(item)
    elif current_grid[1] == limit_max_collumn:
        item = [1,3, 4] #North, South, West
        random1 = random.choice(item)
    elif current_grid[0]%2 <> 0:
        item = [1,2,3,4] #North, East, South, West
        random1 = random.choice(item)
    

elif current_grid[2] == 0 and current_grid[1]%2 <> 0 and current_grid[0] == limit_max_line:
    if  current_grid[1] == limit_min_collumn:
        item = [1,3] #North, South, West        
        random1 = random.choice(item)
    elif current_grid[1] == limit_max_collumn:
        item = [1,2] #North, East, South
        random1 = random.choice(item)
    else:
        item = [1,2,4] #North, East, South, West
        random1 = random.choice(item)

else:
    item = 0
    random1=100
    print("Going ahead")
    

print(item)
print (random1)
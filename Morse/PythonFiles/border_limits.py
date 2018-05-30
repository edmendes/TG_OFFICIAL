# avenue = 0
# crossroad = 1


import random
import math

current_grid=([5, 10, 0]) #must be filled with values given by ros

limit_min_line = 1
limit_max_line = 7

limit_min_collumn = 1
limit_max_collumn = 11


dx = current_grid[0]
dy = curr[1] - current_grid[1]

if current_grid[2] == 0 and current_grid[0] == limit_min_line: #it was in a avenue in line 1
    
    if dy == -1 and dx == 0 and curr[1] == limit_min_collumn:
        random1 = 0 #left
        
    elif dy == -1 and dx == 0:
        item = [0,2] #left or straight 
        random1 = random.choice(item)

    elif dy == 1 and dx == 0 and curr[1] == limit_max_collumn:
        random1 = 1 #right

    elif dy == 1 and dx == 0:
        item = [1,2] #right or straight
        random1 = random.choice(item)

elif current_grid[2] == 0 and current_grid[0] > limit_min_line and current_grid[0] < limit_max_line and current_grid[0]%2==1:
    
    if dy <> 0 and dx == 0 and (curr[1] == limit_min_collumn or curr[1] == limit_max_collumn):
        item = [0,1] #left or right 
        random1 = random.choice(item)
    elif dy <> 0 and dx == 0:
        item = [0,1,2] #left, right or straight
        random1 = random.choice(item)

elif current_grid[2] == 0 and current_grid[0] == limit_max_line: #it was in a avenue in line 1
    
    if dy == -1 and dx == 0 and curr[1] == limit_min_collumn:
        random1 = 1 #right
        
    elif dy == -1 and dx == 0:
        item = [1,2] #right or straight 
        random1 = random.choice(item)

    elif dy == 1 and dx == 0 and curr[1] == limit_max_collumn:
        random1 = 0 #left

    elif dy == 1 and dx == 0:
        item = [0,2] #left or straight
        random1 = random.choice(item)

elif current_grid[2] == 0 and current_grid[1] == limit_min_collumn:
    
    if dx == -1 and dy == 0 and curr[0] == limit_min_line:
        random1 = 1 #right
        
    elif dx == -1 and dy == 0:
        item = [1,2] #right or straight 
        random1 = random.choice(item)

    elif dx == 1 and dy == 0 and curr[0] == limit_max_line:
        random1 = 0 #left

    elif dx == 1 and dy == 0:
        item = [0,2] #left or straight
        random1 = random.choice(item)

elif current_grid[2] == 0 and current_grid[1] > limit_min_collumn and current_grid[1] < limit_max_collumn and current_grid[1]%2==1:
    
    if dx <> 0 and dy == 0 and (curr[0] == limit_min_line or curr[0] == limit_max_line):
        item = [0,1] #left or right 
        random1 = random.choice(item)
    elif dx <> 0 and dy == 0:
        item = [0,1,2] #left, right or straight
        random1 = random.choice(item)

elif current_grid[2] == 0 and current_grid[1] == limit_max_collumn: #it was in a avenue in line 1
    
    if dx == -1 and dy == 0 and curr[0] == limit_min_line:
        random1 = 0 #left
        
    elif dx == -1 and dy == 0:
        item = [0,2] #left or straight 
        random1 = random.choice(item)

    elif dx == 1 and dy == 0 and curr[0] == limit_max_line:
        random1 = 1 #right

    elif dx == 1 and dy == 0:
        item = [1,2] #right or straight
        random1 = random.choice(item)

elif current_grid[2]==1:
    print('do nothing')
    
else:
    print('keep the same')
    random1 = 3

print(dx, dy)
print(random1)

if random1 == 1:
    print('right')
elif random1 == 0:
    print('left')
elif random1 == 2:
    print('straight')
else:
    print('nothing')

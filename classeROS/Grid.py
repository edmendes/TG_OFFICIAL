import numpy as np

D = np.matrix([[-177.211, -160.677, 22.85809, 39.62289, 1, 1, 1], \
[-160.67703, -119.34583, 22.85809, 39.62289,1, 2, 0], \
[-119.34583, -102.81185, 22.85809, 39.62289,1, 3, 1], \
[-102.81185, -36.68525, 22.85809, 39.62289,1, 4, 0], \
[-36.68525, -20.15127, 22.85809, 39.62289,1, 5, 1], \
[-20.15127, 21.17992, 22.85809, 39.62289,1, 6, 0], \
[21.17992, 37.71391, 22.85809, 39.62289,1, 7, 1], \
[37.71391, 103.84052, 22.85809, 39.62289,1, 8, 0], \
[103.84052, 120.37449, 22.85809, 39.62289,1, 9, 1], \
[120.37449, 161.70566, 22.85809, 39.62289,1, 10, 0], \
[161.70566, 178.23965, 22.85809, 39.62289,1, 11, 1], \
[-177.211, -160.677, -21.05104, 20.85703,2, 1, 0]]) 

robot_x = -171.08 #X:-171.08
robot_y = 4.19 #Y:-4.19

V = D[:,:4] #vectorizing D to get all vertices (x1,x2,y1,y2)

Vx = V[:,:2] #get Vx
Vy = V[:,2:] #get Vy

Vx_min = Vx[:,:1]
Vx_max = Vx[:,1:]

Vy_min = Vy[:,:1]
Vy_max = Vy[:,1:]

x_min = np.max(Vx_min[np.where((Vx_min < robot_x))]) # get min x value left to the robot
x_max = np.min(Vx_max[np.where((Vx_max > robot_x))]) # get max x value right to the robot
y_min = np.max(Vy_min[np.where((Vy_min < robot_y))]) # get min y value left to the robot
y_max = np.min(Vy_max[np.where((Vy_max > robot_y))]) # get max x value right to the robot

#grid_location = np.array([x_min, x_max, y_min, y_max]).flatten()
#print(grid_location)
d_index = [np.where((Vx_min == x_min) & (Vx_max == x_max) & (Vy_min == y_min) & (Vy_max == y_max))]
#d_index = [np.where((Vy_max == y_max))]
print(d_index)
grid_state = D[d_index][0][0]
grid = grid_state[:,4:6]
state_type = int(grid_state[:,6:].item(0))

print(grid_state)
print(grid)
print(state_type)
"""
print(Vx_min)
print(Vx_max)
print(Vy_min)
print(Vy_max)
"""

#grid_state = V_grid_elements[:,4:]

#print(grid_location)

#state_type = int(grid_state[:,2].item(0))

#print(state_type)
"""
print(Vx_min[np.where(Vx_min < robot_x)])
print(Vx_max[np.where(Vx_max > robot_x)])
print(Vy_min[np.where(Vy_min < robot_y)])
print(Vy_max[np.where(Vy_max > robot_y)])


#define the robot state for the current grid
r_dimension_x = np.abs(np.abs(x_max) - np.abs(x_min)) # calculate x dimension
r_dimension_y = np.abs(np.abs(y_max) - np.abs(y_min)) # calculate y dimension
r_dimension = r_dimension_y / r_dimension_x  #calculate the relation between x and y dimension 

#if relation = 1 then the state is in a crossroad (left-right-ahead actions required)
if(np.around(r_dimension, 2) == 1.00):
    print(r_dimension)

#otherwise the robot is in a simple avenue (ahead action required)
else:
    """ 
print(x_min)
print(x_max)
print(y_min)
print(y_max)

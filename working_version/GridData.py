#!/usr/bin/env python
import numpy as np

class GridData():
            
    #The __init__ method defines the object instantiation operation
    def __init__(self):
        """
        Others attributes instances 
        """
        self.valid_actions = [1, 2, 4]

    def get_grid_state(self,robot_x, robot_y):
        """
        /BEGIN - THIS PART NEEDS TO BE READABLE ONLY ONCE -- PRE-PROCESSED
        """
        # 61x7 D matrix instance with x1,x2,y1,y2 vertices and grid_row, grid_col, state_type values (non-repeatable) in each row
        D = np.matrix([[-178.02, -161.49, 20.29, 36.82,1,1, 1], \
        [-161.49, -120.16, 20.29, 36.82,1,2, 0], \
        [-120.16, -103.62, 20.29, 36.82,1,3, 1], \
        [-103.62, -37.5, 20.29, 36.82,1,4, 0], \
        [-37.5, -20.96, 20.29, 36.82,1,5, 1], \
        [-20.96, 20.36, 20.29, 36.82,1,6, 0], \
        [20.36, 36.89, 20.29, 36.82,1,7, 1], \
        [36.89, 103.02, 20.29, 36.82,1,8, 0], \
        [103.02, 119.55, 20.29, 36.82,1,9, 1], \
        [119.55, 160.88, 20.29, 36.82,1,10, 0], \
        [160.88, 177.42, 20.29, 36.82,1,11, 1], \
        [-178.02, -161.49, -21.01, 20.29,2,1, 0], \
        [-120.16, -103.62, -21.01, 20.29,2,3, 0], \
        [-37.5, -20.96, -21.01, 20.29,2,5, 0], \
        [20.36, 36.89, -21.01, 20.29,2,7, 0], \
        [103.02, 119.55, -21.01, 20.29,2,9, 0], \
        [160.88, 177.42, -21.01, 20.29,2,11, 0], \
        [-178.02, -161.49, -37.54, -21.01,3,1, 1], \
        [-161.49, -120.16, -37.54, -21.01,3,2, 0], \
        [-120.16, -103.62, -37.54, -21.01,3,3, 1], \
        [-103.62, -37.5, -37.54, -21.01,3,4, 0], \
        [-37.5, -20.96, -37.54, -21.01,3,5, 1], \
        [-20.96, 20.36, -37.54, -21.01,3,6, 0], \
        [20.36, 36.89, -37.54, -21.01,3,7, 1], \
        [36.89, 103.02, -37.54, -21.01,3,8, 0], \
        [103.02, 119.55, -37.54, -21.01,3,9, 1], \
        [119.55, 160.88, -37.54, -21.01,3,10, 0], \
        [160.88, 177.42, -37.54, -21.01,3,11, 1], \
        [-178.02, -161.49, -103.65, -37.54,4,1, 0], \
        [-120.16, -103.62, -103.65, -37.54,4,3, 0], \
        [-37.5, -20.96, -103.65, -37.54,4,5, 0], \
        [20.36, 36.89, -103.65, -37.54,4,7, 0], \
        [103.02, 119.55, -103.65, -37.54,4,9, 0], \
        [160.88, 177.42, -103.65, -37.54,4,11, 0], \
        [-178.02, -161.49, -120.17, -103.65,5,1, 1], \
        [-161.49, -120.16, -120.17, -103.65,5,2, 0], \
        [-120.16, -103.62, -120.17, -103.65,5,3, 1], \
        [-103.62, -37.5, -120.17, -103.65,5,4, 0], \
        [-37.5, -20.96, -120.17, -103.65,5,5, 1], \
        [-20.96, 20.36, -120.17, -103.65,5,6, 0], \
        [20.36, 36.89, -120.17, -103.65,5,7, 1], \
        [36.89, 103.02, -120.17, -103.65,5,8, 0], \
        [103.02, 119.55, -120.17, -103.65,5,9, 1], \
        [119.55, 160.88, -120.17, -103.65,5,10, 0], \
        [160.88, 177.42, -120.17, -103.65,5,11, 1], \
        [-178.02, -161.49, -161.49, -120.17,6,1, 0], \
        [-120.16, -103.62, -161.49, -120.17,6,3, 0], \
        [-37.5, -20.96, -161.49, -120.17,6,5, 0], \
        [20.36, 36.89, -161.49, -120.17,6,7, 0], \
        [103.02, 119.55, -161.49, -120.17,6,9, 0], \
        [160.88, 177.42, -161.49, -120.17,6,11, 0], \
        [-178.02, -161.49, -178.02, -161.49,7,1, 1], \
        [-161.49, -120.16, -178.02, -161.49,7,2, 0], \
        [-120.16, -103.62, -178.02, -161.49,7,3, 1], \
        [-103.62, -37.5, -178.02, -161.49,7,4, 0], \
        [-37.5, -20.96, -178.02, -161.49,7,5, 1], \
        [-20.96, 20.36, -178.02, -161.49,7,6, 0], \
        [20.36, 36.89, -178.02, -161.49,7,7, 1], \
        [36.89, 103.02, -178.02, -161.49,7,8, 0], \
        [103.02, 119.55, -178.02, -161.49,7,9, 1], \
        [119.55, 160.88, -178.02, -161.49,7,10, 0], \
        [160.88, 177.42, -178.02, -161.49,7,11, 1]
        ]) 
        
        V = D[:,:4] #vectorizing D to get all vertices (x1,x2,y1,y2)

        Vx = V[:,:2] #get Vx - vertices of x axis from V matrix
        Vy = V[:,2:] #get Vy - vertices of y axis from V matrix

        Vx_min = Vx[:,:1] #get first column related to min values of x axis (right 2xn)
        Vx_max = Vx[:,1:] #get second column related to max values of x axis (left xn)

        Vy_min = Vy[:,:1] #get first column related to min values of y axis (right 2xn)
        Vy_max = Vy[:,1:] #get second column related to max values of y axis (left 2x)
        """
        /END - THIS PART NEEDS TO BE READABLE ONLY ONCE -- PRE-PROCESSED
        """
        #get x and y interval values corresponding to the robot position
        x_min = np.max(Vx_min[np.where((Vx_min < robot_x))]) # get min x value left to the robot
        x_max = np.min(Vx_max[np.where((Vx_max > robot_x))]) # get max x value right to the robot
        y_min = np.max(Vy_min[np.where((Vy_min < robot_y))]) # get min y value left to the robot
        y_max = np.min(Vy_max[np.where((Vy_max > robot_y))]) # get max x value right to the robot

        d_index = [np.where((Vx_min == x_min) & (Vx_max == x_max) & (Vy_min == y_min) & (Vy_max == y_max))]
        grid_state = D[d_index][0] #consider this line if you have numpy new version 
        #grid_state = D[d_index][0][0] #consider this line if you have numpy old version
        grid = grid_state[:,4:6]
        #state_type = int(grid_state[:,6:].item(0))

        #define the robot state for the current grid
        r_dimension_x = np.abs(np.abs(x_max) - np.abs(x_min)) # calculate x dimension
        r_dimension_y = np.abs(np.abs(y_max) - np.abs(y_min)) # calculate y dimension
        r_dimension = r_dimension_y / r_dimension_x #calculate the relation between x and y dimension 

        #if relation = 1 then the state is in a crossroad (left-right-ahead actions required)
        if(np.around(r_dimension,1) == 1.0):
            state = 0 #"crossroad"
        #otherwise the robot is in a simple avenue (ahead action required)
        else:
            state = 1 #"avenue"
        return x_min, x_max, y_min, y_max, grid, state
    

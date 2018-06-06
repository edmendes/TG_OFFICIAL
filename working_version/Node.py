#!/usr/bin/env python
import rospy
import json
import random
import sys
import time
import math
from math import atan2
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from GridData import GridData
from BorderLimits import BorderLimits
from Brain import Brain
from Memory import Memory
from pynput.keyboard import Key, Controller
from time import localtime, strftime


"""
Global variables
"""
deltaX = 0.0; deltaY =0.0; direction_factor = 0; diffx = 0.0; diffy = 0.0; previousError = 0.0; Integral = 0.0 #buffers
laser_x1 =0.0; laser_x2 = 0.0 #buffers
num1 = 0.0; num2 =0; ref2 = 0.0 #iteration

class Node():
    #The __init__ method defines the object instantiation operation
    def __init__(self):
        
        """
        Instances for each Publisher (ignore this part for a while)
        """
        #self.distance_publisher = rospy.Publisher('dist',std_msgs.msg, queue_size=10)

        """  
        Attributes instances for each Subscriber and Publisher, corresponding to each ATVR sensor topic
        """ 
        self.pose_subscriber = rospy.Subscriber("/pose", PoseStamped, self.callback_pose)
        self.scan_subscriber = rospy.Subscriber('/scan', LaserScan, self.callback_laser)
        self.scan1_subscriber = rospy.Subscriber('/scan1', LaserScan, self.callback_laser1)        
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

        """  
        Attributes instances for sensors' parameters
        """
        self.pose = PoseStamped()
        self.laser = LaserScan()
        self.laser1 = LaserScan()
        self.speed = Twist()
        self.rate = rospy.Rate(4) #attribute for Rate in Hz (velocity in which the messages will be received by Subscribers) 

        """
        Others attributes instances 
        """
        self.heading_angle = 0.0
        self.bearing_angle = 0.0
        self.direction_factor = 0
        self.wind_rose = 0      #wind_rose is responsible to store the last state when the car is in a crossroad

    """
    Subscribers callback methods
    """
    # method to get pose messages
    def callback_pose(self, msg):

        self.pose = msg #update pose attribute with msg returned by sensor
        self.pose.pose.position.x = round(self.pose.pose.position.x, 3)
        self.pose.pose.position.y = round(self.pose.pose.position.y, 3)
        
        quaternion = (
            self.pose.pose.orientation.x,
            self.pose.pose.orientation.y,
            self.pose.pose.orientation.z,
            self.pose.pose.orientation.w
        )

        euler = euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        self.heading_angle = euler[2]
    
    # method to get laser messages - frontal
    def callback_laser(self, msg):
        self.laser = msg
        self.laser.ranges
        self.laser.angle_increment

    # method to get laser1 messages - corner
    def callback_laser1(self, msg):
        self.laser1 = msg
        self.laser1.ranges

    """
    Starting sensors processing
    """
    def laser_information(self, laser_raw, angle_increment):
    
        try:
            index_min = min(xrange(len(laser_raw)), key=laser_raw.__getitem__) #get the vector number which contains the minimum value of the range mentioned above

            total_array = len(laser_raw)+1 #count the total amount of vectors 
            angle_segment = angle_increment #this is the angle between each vector

            half_total_array = total_array/2 #in order to get the middle range
            
            index_value = index_min - half_total_array
            angle_to_object = angle_segment*(index_value) # to check the angle between range 0 and the middle one
            min_range = min(laser_raw) #the minimum value between car and the object
            
            return index_value, angle_to_object, min_range

        except (ValueError, TypeError):
            return 0, 0, 0

    def laser1_information(self, laser_raw1):

        try: 
            index_min = min(xrange(len(laser_raw1)), key=laser_raw1.__getitem__) #get the vector number which contains the minimum value of the range mentioned above
            index_max = max(xrange(len(laser_raw1)), key=laser_raw1.__getitem__) 
            lateral_laser= laser_raw1[index_min]
            lateral_laser_max = laser_raw1[index_max]
            
            return lateral_laser, lateral_laser_max        
        
        except (ValueError, TypeError):
            return 0, 0

    def object_scenary_position(self, index_value, angle_to_object, min_range, direction_factor, pose_x, pose_y):

        if direction_factor == 1:
            extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
            extra_y = math.cos(angle_to_object)*min_range
            self.wind_rose = direction_factor #wind_rose = 1 - Going North

            if index_value > 0:
                object_position_x = math.floor(pose_x-extra_x)
                object_position_y = math.ceil(pose_y+extra_y)
            else: 
                object_position_x = math.ceil(pose_x+extra_x)
                object_position_y = math.ceil(pose_y+extra_y)

        elif direction_factor == 2:
            extra_x = math.cos(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
            extra_y = math.sin(angle_to_object)*min_range
            self.wind_rose = direction_factor #wind_rose = 2 - Going East

            if index_value > 0:
                object_position_x = math.ceil(pose_x+extra_x)
                object_position_y = math.ceil(pose_y+extra_y)
            else: 
                object_position_x = math.ceil(pose_x+extra_x)
                object_position_y = math.floor(pose_y-extra_y)
            
        elif direction_factor == 3:
            extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
            extra_y = math.cos(angle_to_object)*min_range
            self.wind_rose = direction_factor #wind_rose = 3 - Going South

            if index_value > 0:
                object_position_x = math.ceil(pose_x+extra_x)
                object_position_y = math.floor(pose_y-extra_y)
            else: 
                object_position_x = math.floor(pose_x-extra_x)
                object_position_y = math.floor(pose_y-extra_y)
            
        elif direction_factor == 4:
            extra_x = math.cos(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
            extra_y = math.sin(angle_to_object)*min_range
            self.wind_rose = direction_factor #wind_rose = 4 - Going West

            if index_value > 0:
                object_position_x = math.floor(pose_x-extra_x)
                object_position_y = math.floor(pose_y-extra_y)
            else: 
                object_position_x = math.floor(pose_x-extra_x)
                object_position_y = math.ceil(pose_y+extra_y)
              
        else:
            extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
            extra_y = math.cos(angle_to_object)*min_range

            if index_value > 0:
                object_position_x = 10000
                object_position_y = 10000
            else: 
                object_position_x = 10000
                object_position_y = 10000
                         
        distance_between_objects_x = object_position_x-pose_x
        distance_between_objects_y = object_position_y-pose_y

        return distance_between_objects_x, distance_between_objects_y 
    
    def PID(self, wanted_value, current_value):
        
        global previousError, Integral
        
        Kp = 0.5 #this constants were attributed based on tests. 
        Ki = 0.001
        Kd = 0.05
    
        error = wanted_value - current_value
        Proportional = error
        Integral = Integral + error
        Differential = error - previousError

        PIDvalue = (Kp*Proportional) + (Ki*Integral) + (Kd*Differential)
        previousError = abs(error) - abs(previousError)

        return PIDvalue      

    """
    Starting movement actions 
    """
    def direction(self, pose_x, pose_y):
        global num1                                             #iteration
        global old_position_x, old_position_y, deltaX, deltaY    #buffers

        tolerance_angle = 0.2

        if (num1 < 2):  #the num1 is a buffer, the value of x and y should be stored for 0.03s to compare to a current value.
            old_position_x = pose_x
            old_position_y = pose_y
            time.sleep(0.01)
            #print("This is x: %.2f and this is y: %.2f" %(old_position_x,old_position_y))
            num1 = num1 + 1

        elif (num1 >= 2 and num1 <= 4):
            
            time.sleep(0.01)
            num1 = num1 + 1

        else:
            deltaX =  pose_x - old_position_x #deltaX is the x position difference between present and a moment 0.05s ago 
            deltaY = pose_y - old_position_y #deltaY is the y position difference between present and a moment 0.05s ago
            """print("This is x2: %.4f and this is x1: %.4f,DeltaX: %.4f" %(pose_x, old_position_x,deltaX))
            print("This is y2: %.4f and this is y1: %.4f, DeltaY: %.4f " %(pose_y, old_position_y, deltaY))"""
            num1 = 0

            if (deltaX > -tolerance_angle and deltaX < tolerance_angle  and deltaY > tolerance_angle ): #in this case x do not change too much and y is increasing faster which indicates that the car is going to North
                self.direction_factor = 1
            elif(deltaX > tolerance_angle  and deltaY> -tolerance_angle and  deltaY < tolerance_angle ):#in this case y do not change too much and x is increasing faster which indicates that the car is going to East
                self.direction_factor = 2
            elif(deltaX > - tolerance_angle  and deltaX < tolerance_angle  and deltaY < -tolerance_angle  ): #in this case x do not change too much and y is decreasing faster which indicates that the car is going to South
                self.direction_factor = 3
            elif(deltaX < -tolerance_angle  and deltaY > - tolerance_angle  and deltaY < tolerance_angle  ): #in this case y do not change too much and x is decreasing faster which indicates that the car is going West
                self.direction_factor = 4
            else :
                self.direction_factor = 5 #an exception to all those cases
    
    def wind_rose_function(self, wind_rose, objective_wind_rose):

        final_choice = 100
        last_state = wind_rose #consider the last_state, i. e. before it enter in crossroad zone it store the direction (north, east, south, west) of last movement

        if (objective_wind_rose == 1): #it is the direction objetive: 1 - North

            if(last_state == 1):    #I'm going North and I want to keep going North
                final_choice = 3    #Go Ahead
            elif (last_state == 2): #I'm going East and I want to going North
                final_choice = 0    #Turn_Left
            elif (last_state == 3): #I'm going South and I want to going North
                final_choice = 2    #U-Turn
            elif (last_state == 4): #I'm going Westand I want to going North
                final_choice = 1    #Turn_Right
        
        elif (objective_wind_rose == 2): #it is the direction objetive: 2 - East

            if(last_state == 1):    #I'm going North and I want to going East
                final_choice = 1    #Turn_Right
            elif (last_state == 2): #I'm going East and I want to going East
                final_choice = 3    #Go Ahead
            elif (last_state == 3): #I'm going South and I want to going East
                final_choice = 0    #Turn_Left
            elif (last_state == 4): #I'm going West and I want to going East
                final_choice = 2    #U-Turn
        
        elif (objective_wind_rose == 3): #it is the direction objetive: 3 - South

            if(last_state == 1):
                final_choice = 2    #U-Turn
            elif (last_state == 2):
                final_choice = 1    #Turn_Right
            elif (last_state == 3):
                final_choice = 3    #Go Ahead
            elif (last_state == 4):
                final_choice = 0    #Turn_Left

        elif (objective_wind_rose == 4): #it is the direction objetive: 4 - West
            if(last_state == 1):
                final_choice = 0    #Turn_Left
            elif (last_state == 2):
                final_choice = 2    #U-Turn
            elif (last_state == 3):
                final_choice = 1    #Turn_Right
            elif (last_state == 4): 
                final_choice = 3     #Go Ahead               
        else:
            pass
            #print("do nothing")

        return final_choice
   
    def turning_around(self, distance_between_objects_x, distance_between_objects_y,wind_rose, final_choice):

        #wind_rose: 1 - North, 2 - East, 3 - South, 4 -West
        #bearing_angle #it is the angle which needed to make the car be directed to the objective, for example to North for West the desired angle is math.pi()
        
        global ref2 #responsible to check if the car is going straight or curve
        global diffx, diffy #it is the abs value of distance between car and object. 
        
        print("Initiating the turning left or right movement...")
        turn_choose = final_choice #zero indicates that the car intend to turn left, 1 turn right and 2 move ahead. 
        
        if ref2 < 1: #ref2 is responsile to keep the diffx and diffy the same until complete the turning process
            diffx = abs(distance_between_objects_x) # returns the distance between the car and the object
            diffy = abs(distance_between_objects_y)
        else:
            diffy = diffy
            diffx = diffx

        angle_objective = abs(self.bearing_angle - self.heading_angle)

        if(wind_rose==1 and turn_choose==0 and diffy < 12): #Going North, Turn Right, DeltaY between object and car is 12
            ref2 = 1    #started process of turning around
            self.bearing_angle = math.pi #in this case heading angle is pi/2. Thus, to go to West, it needs to turn right til reach pi.

            if abs(angle_objective) > 0.1: #Turning Right until bearing angle-heading angle be less than 0.1
                print("Xo1")
                
                self.speed.linear.x = 1.2
                self.speed.angular.z = 0.3
                
            else:
                ref2 = 0
                
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                
                time.sleep(0.1) #not sure if it is necessary
        
        elif(wind_rose==1 and turn_choose==1 and diffy < 12): #Going North, Turn Left, DeltaY between object and car is 12
            ref2 = 1
            self.bearing_angle = 0

            if abs(angle_objective) > 0.1:
                print("Xo1")
                
                self.speed.linear.x = 2
                self.speed.angular.z = -0.3
                
            else:
                ref2 = 0
                
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                
                time.sleep(0.1)

        elif(wind_rose==2 and turn_choose==0 and diffx < 12): #Going East, Turn Right, DeltaY between object and car is 12   
            ref2 = 1
            self.bearing_angle = math.pi/2

            if abs(angle_objective) > 0.1:
                print("Xo2")
                
                self.speed.linear.x = 1.3
                self.speed.angular.z = 0.3
                
            else:
                ref2 = 0
                
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                
                time.sleep(0.1)

        elif(wind_rose==2 and turn_choose==1 and diffx < 12): #Going East, Turn Left, DeltaY between object and car is 12    
            ref2 = 1
            self.bearing_angle = -math.pi/2

            if abs(angle_objective) > 0.1:
                print("Xo2")
                
                self.speed.linear.x = 2
                self.speed.angular.z = -0.3
                
            else:
                ref2 = 0
                
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                
                print(self.speed.angular.z)
                time.sleep(0.1)
        
        elif(wind_rose==3 and turn_choose==0 and diffy < 12): #Going South, Turn Right, DeltaY between object and car is 12    
            ref2 = 1
            self.bearing_angle = 0

            if abs(angle_objective) > 0.1:
                print("Xo3")
                
                self.speed.linear.x = 1.3
                self.speed.angular.z = 0.3
            
            else:
                ref2 = 0
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                time.sleep(0.1)

        elif(wind_rose==3 and turn_choose==1 and diffy < 12): #Going South, Turn Left, DeltaY between object and car is 12   
            ref2 = 1
            self.bearing_angle = -math.pi

            if abs(angle_objective) > 0.1:
                print("Xo3")
                self.speed.linear.x = 2
                self.speed.angular.z = -0.3
            else:
                ref2 = 0
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                time.sleep(0.1)

        elif(wind_rose==4 and turn_choose==0 and diffx < 12): #Going West, Turn Right, DeltaY between object and car is 12    
            ref2 = 1
            self.bearing_angle = -math.pi/2

            if abs(angle_objective) > 0.1:
                print("Xo4")
                self.speed.linear.x = 1.3
                self.speed.angular.z = 0.3
            else:
                ref2 = 0
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                time.sleep(0.1)

        elif(wind_rose==4 and turn_choose==1 and diffx < 12): #Going West, Turn Left, DeltaY between object and car is 12    
            ref2 = 1
            self.bearing_angle = math.pi/2

            if abs(angle_objective) > 0.1:
                print("Xo4")
                self.speed.linear.x = 2
                self.speed.angular.z = -0.3
            else:
                ref2 = 0
                self.speed.linear.x = 1.0
                self.speed.angular.z = 0.0
                print(self.speed.angular.z)
                time.sleep(0.1)

        elif   (turn_choose==2):
            self.speed.linear.x = 1.7
            self.speed.angular.z = -0.8

        else:
            self.speed.linear.x = 1
            self.speed.angular.z = 0
        
        """print(wind_rose) #the last direction value , North, East, South, West
        #print(turn_choose) #0 Turn Left, 1 Turn Right
        print(diffx,diffy) #Distance Between Object and the car
        print(angle_objective) #Angle that a want to reach
        print(bearing_angle)
        print(heading_angle)"""

        self.pub.publish(self.speed)
        self.rate.sleep()   
        
    def detecting_sidewalk(self, lateral_laser, lateral_laser_max, distance_between_objects_x, distance_between_objects_y, wind_rose, turn_choice):
        
        global num2, laser_x1, laser_x2

        desired_angle = 0.0

        if turn_choice == 0: #this was used to give the curve moment a smoothly movement
            minimum_laser_difference = 2
            laser_max_option = 4
        
        elif turn_choice == 1:
            minimum_laser_difference =1
            laser_max_option = 4.9

        elif turn_choice == 2:
            minimum_laser_difference = 1
            laser_max_option = 4.9
        else: 
            minimum_laser_difference = 1
            laser_max_option = 4.9

        
        if num2 < 1:
            laser_x1 = lateral_laser #minimum distance between car an sidewalk
            #time.sleep(0.1)
            num2 = num2 +1 #wind_rose to check the laser minimum distance in different moments

        elif num2 == 1:
            laser_x2 = lateral_laser - laser_x1 #it is the difference between two different moments
            num2 = 0

        #diff_lateral_laser = lateral_laser_max - lateral_laser    
        print("Lateral laser %.5f" %lateral_laser)
        """print("Lateral Max %.5f" %lateral_laser_max)
        print(laser_x1)
        print(laser_x2)"""

        if lateral_laser_max <= laser_max_option and laser_x2 < minimum_laser_difference: #if the car follow these statements it should go straight or should correct it movement to go straight
            if self.heading_angle > (-math.pi/2-0.75) and self.heading_angle < (-math.pi/2+0.75): #if the heading angle is between this values, the car is going West, so the heading angle must be directed to -pi/2
                desired_angle = -math.pi/2
            elif self.heading_angle > (-0.75) and self.heading_angle < (0.75):
                desired_angle = 0
            elif self.heading_angle > (math.pi/2-0.75) and self.heading_angle < (math.pi/2+0.75):
                desired_angle = math.pi/2
            elif self.heading_angle > (math.pi -0.75) and self.heading_angle < (math.pi+0.75) :
                desired_angle = math.pi
            elif self.heading_angle >= (-math.pi) and self.heading_angle <(-math.pi + 0.75):
                desired_angle = -math.pi
            else:
                desired_angle = desired_angle

            pid_angle = self.PID(desired_angle, self.heading_angle) #controller to keep the car near to the desired angle
            pid_straight_line = self.PID(2, lateral_laser) #contoreller to keep the car in a proper distance to the sidewalk

            if lateral_laser < 1.90 or (lateral_laser > 2.1 and lateral_laser < 4.5):
                self.speed.linear.x = 1 + pid_angle - pid_straight_line
                self.speed.angular.z = pid_angle - pid_straight_line 
            
            elif lateral_laser > 5.0:
                self.speed.linear.x = 0
                self.speed.angular.z = 0
            
            else:  #final adjustments, when the car is almost riding straigh it keeps it going straight
                if laser_x2 < -0.001:
                    self.speed.linear.x = 1
                    self.speed.angular.z = -0.02

                elif laser_x2 > 0.001:
                    self.speed.linear.x = 1
                    self.speed.angular.z = 0.02
                
                else: 
                    self.speed.linear.x = 1
                    self.speed.angular.z = 0.00

            """print("pid_angle: %.5f"%pid_angle)
            print("pid_straight_line: %.5f"%pid_straight_line)
            print(speed.angular.z)"""

        else: 
            self.turning_around(distance_between_objects_x, distance_between_objects_y, wind_rose, turn_choice)
    
        self.pub.publish(self.speed)
        self.rate.sleep()
 
    """
    Starting and processing ROS Node
    """
    def agent_go(self):
        action= 0
        step = 0
        state_row_next = 100
        state_col_next =100
        reward = 0
        curr_episode = 0
        """
        /BEGIN - setting data to process episode results 
        """
        start_time = strftime("%Y-%m-%d %H:%M:%S", localtime()) #get the start datetime of n-episode (n=1,2,3,4...) -- control effects
        start_point = "Start1" #set the start point -- control the policy to follow
        """
        /END - setting data to process episode results 
        """
        while not rospy.is_shutdown():
            #print "robot position: (X:%.2f Y:%.2f)" % (self.pose.pose.position.x, self.pose.pose.position.y) 
            
            x_min, x_max, y_min, y_max, state, road_type = grid.get_grid_state(self.pose.pose.position.x, self.pose.pose.position.y)
            """
            Check if robot is in a grid and get which one is current
            """
            curr_episode = memory.get_last_episode() #get current episode of learning trial
            if (x_min < self.pose.pose.position.x < x_max) and (y_min < self.pose.pose.position.y < y_max):
                try:
                    if action == 100 and road_type == 0: # the reaches the crossroad for the first time
                        action = limits.border_limit(state[:,:1].item(0),state[:,1:2].item(0), road_type) #get an action randomly using the current state
                        state_row_next, state_col_next = brain.get_next_state(state[:,:1].item(0),state[:,1:2].item(0), action) #preview the next state due to current action in the current state
                        reward = brain.get_reward(state[:,:1].item(0),state[:,1:2].item(0)) #get the reward accordingly with the current state
                        brain.update_qtable(state[:,:1].item(0),state[:,1:2].item(0), action, reward, state_row_next, state_col_next)
                        step = step + 1 #sum the amount of steps
                        if(reward == 100):
                            last_tableQ = brain.get_matrixQ()
                            memory.reset_agent(step, curr_episode, start_point, start_time, last_tableQ)
                            step = 0
                            start_time = strftime("%Y-%m-%d %H:%M:%S", localtime()) #get the start datetime of n-episode (n=1,2,3,4...) -- control effects
                        Controller().release(Key.f11)
                        
                    elif road_type == 1:
                        print(state)
                        print(state)
                        action = 100
                        state_row_next, state_col_next = state_row_next, state_col_next
                        reward = reward
                    else:
                        action = action
                        state_row_next, state_col_next = state_row_next, state_col_next
                        reward = reward
                
                
                except IndexError:
                    action = 100
                    pass 

                #print state#"Im in a grid and my state is %s and grid %s" % (state, grid)
                """
                if true, the moviment is started
                """
                
                index_value, angle_to_object, min_range = self.laser_information(self.laser.ranges, self.laser.angle_increment)
                #print(index_value, angle_to_object, min_range)

                lateral_laser, lateral_laser_max = self.laser1_information(self.laser1.ranges)
                #print(lateral_laser, lateral_laser_max)

                self.direction(self.pose.pose.position.x, self.pose.pose.position.y) #show what direction car is going
                
                distance_between_objects_x, distance_between_objects_y = self.object_scenary_position(index_value, angle_to_object, min_range, self.direction_factor, self.pose.pose.position.x, self.pose.pose.position.y)
                
                final_choice = self.wind_rose_function(self.wind_rose, action) #second attribute: 1 - Want to go North, 2 - Want to go East, 3 - Want to go South, 4 - Want to go West #choice is the Q learning option
                                                                    
                self.detecting_sidewalk(lateral_laser, lateral_laser_max, distance_between_objects_x, distance_between_objects_y, self.wind_rose, final_choice)
                
                print("Direction choice: %d" %action)
                #print("Steps %d" %step)

                #print("Going to State (%d, %d), the previous reward was %d" %(state_row_next, state_col_next, reward))
                #print("Current State (%d, %d)" %(state[:,:1].item(0),state[:,1:2].item(0)))
            

            else:
                print "Im out of a grid -- something wrong is happening"
            
            self.rate.sleep()

if __name__=='__main__':   
    rospy.init_node("sensor_node") #iniciate ROS node
    sensor_node = Node() #instance the Node class as an object named as sensor_node
    grid = GridData() #instance the GridData class as an object named as grid
    brain =  Brain() #instance the Brain class as an object named as brain
    limits = BorderLimits() #instance the BorderLimits class as an object named as limits
    memory = Memory() #instance the Memory class as an object named as memory
    sensor_node.agent_go() #1 - North, 2 - East, 3 - South, 4 - West
    
    
#!/usr/bin/env python

import rospy
import json
import sys
import time
import math
import operator
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from math import atan2
import numpy as np

deltaX = 0.0; deltaY =0.0; direction_factor = 0;  #buffers
num1 = 0.0 #iteration

class Agent():
    
    def __init__(self):
        self.init_node = rospy.init_node("speed_controller")
        
        self.pose_subscriber = rospy.Subscriber("/pose", PoseStamped, self.callback_pose)
        self.scan_subscriber = rospy.Subscriber('/scan', LaserScan, self.callback_laser)
        self.scan1_subscriber = rospy.Subscriber('/scan1', LaserScan, self.callback_laser1)        

        self.pose = PoseStamped()
        self.laser = LaserScan()
        self.laser1 = LaserScan()
        self.speed = Twist()
        self.rate = rospy.Rate(4)
        
        self.heading_angle = 0.0
        self.direction_factor = 0
        self.wind_rose = 0      #wind_rose is responsible to store the last state when the car is in a crossroad
        

    def callback_pose(self, msg):

        self.pose = msg
        self.pose.pose.position.x
        self.pose.pose.position.y
        
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
    
    def callback_laser(self, msg):
        
        self.laser = msg
        self.laser.ranges
        self.laser.angle_increment

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
        
    def callback_laser1(self, msg):
        self.laser1 = msg
        self.laser1.ranges
    
    def laser1_information(self, laser_raw1):

        try: 
            index_min = min(xrange(len(laser_raw1)), key=laser_raw1.__getitem__) #get the vector number which contains the minimum value of the range mentioned above
            index_max = max(xrange(len(laser_raw1)), key=laser_raw1.__getitem__) 
            lateral_laser= laser_raw1[index_min]
            lateral_laser_max = laser_raw1[index_max]
            
            return lateral_laser, lateral_laser_max
        
        
        except (ValueError, TypeError):
            return 0, 0

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

        """print("extra x: %.4f, extra y: %.4f" %(extra_x, extra_y))
        print("object_position_x: %.4f, object_position_y: %.4f" %(object_position_x,object_position_y))
        print("distance_between_objects_x: %.4f" %distance_between_objects_x)
        print("distance_between_objects_y: %.4f" %distance_between_objects_y)"""

        return distance_between_objects_x, distance_between_objects_y     

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
            print("do nothing")

        return final_choice



    def agent_action(self):
        rospy.loginfo("Estoy Ca")
        
        while not rospy.is_shutdown():

            #print("robot position: (X:%.2f Y:%.2f, Heading_angle: %.2f" % (self.pose.pose.position.x, self.pose.pose.position.y, self.heading_angle))
            
            index_value, angle_to_object, min_range = self.laser_information(self.laser.ranges, self.laser.angle_increment)
            #print(index_value, angle_to_object, min_range)

            lateral_laser, lateral_laser_max = self.laser1_information(self.laser1.ranges)
            #print(lateral_laser, lateral_laser_max)

            self.direction(self.pose.pose.position.x, self.pose.pose.position.y) #show what direction car is going
            
            distance_between_objects_x, distance_between_objects_y = self.object_scenary_position(index_value, angle_to_object, min_range, self.direction_factor, self.pose.pose.position.x, self.pose.pose.position.y)
            
            choice = self.wind_rose_function(self.wind_rose, 1) #second attribute: 1 - Want to go North, 2 - Want to go East, 3 - Want to go South, 4 - Want to go West
                                                                #choice is the Q learning option
            print("Where I want to go %d" %choice) 
            print(self.direction_factor, deltaX, deltaY)
            print(distance_between_objects_x, distance_between_objects_y, self.wind_rose)

            self.rate.sleep()
        rospy.spin()

if __name__=='__main__':

    rospy.init_node("speed_controller")
    agent = Agent()
    agent.agent_action()
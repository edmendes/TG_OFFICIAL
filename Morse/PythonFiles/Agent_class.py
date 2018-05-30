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

deltaX = 0.0; deltaY =0.0; direction_factor = 0;  
num1 = 0.0

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
        global num1 
        global old_position_x, old_position_y, deltaX, deltaY, direction_factor     

        tolerance_angle = 0.2

        if (num1 < 2): #the num1 is a buffer, the value of x and y should be stored for 0.03s to compare to a current value.
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
                direction_factor = 1
            elif(deltaX > tolerance_angle  and deltaY> -tolerance_angle and  deltaY < tolerance_angle ):#in this case y do not change too much and x is increasing faster which indicates that the car is going to East
                direction_factor = 2
            elif(deltaX > - tolerance_angle  and deltaX < tolerance_angle  and deltaY < -tolerance_angle  ): #in this case x do not change too much and y is decreasing faster which indicates that the car is going to South
                direction_factor = 3
            elif(deltaX < -tolerance_angle  and deltaY > - tolerance_angle  and deltaY < tolerance_angle  ): #in this case y do not change too much and x is decreasing faster which indicates that the car is going West
                direction_factor = 4
            else :
                direction_factor = 5 #an exception to all those cases

            
        
        

    def agent_action(self):
        rospy.loginfo("Estoy Ca")
        
        while not rospy.is_shutdown():

            #print("robot position: (X:%.2f Y:%.2f, Heading_angle: %.2f" % (self.pose.pose.position.x, self.pose.pose.position.y, self.heading_angle))
            
            index_value, angle_to_object, min_range = self.laser_information(self.laser.ranges, self.laser.angle_increment)
            #print(index_value, angle_to_object, min_range)

            lateral_laser, lateral_laser_max = self.laser1_information(self.laser1.ranges)
            #print(lateral_laser, lateral_laser_max)

            self.direction(self.pose.pose.position.x, self.pose.pose.position.y)
            
            print(direction_factor, deltaX, deltaY)

            self.rate.sleep()
        rospy.spin()

if __name__=='__main__':

    rospy.init_node("speed_controller")
    agent = Agent()
    agent.agent_action()
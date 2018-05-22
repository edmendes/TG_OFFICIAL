#!/usr/bin/env python

import rospy
import json
import time
import math
import operator
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
import numpy as np



# get the laser messages
def newOdom(msg):
    global x
    global y
    global heading_angle

    x = msg.pose.position.x
    y = msg.pose.position.y

    quaternion = (
        msg.pose.orientation.x,
        msg.pose.orientation.y,
        msg.pose.orientation.z,
        msg.pose.orientation.w)
    euler = euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    heading_angle = euler[2]


def callback_laser(msg):
    global curr_pose
    angle_segment = 0

    laser_raw = msg.ranges
    index_min = min(xrange(len(laser_raw)), key=laser_raw.__getitem__)
    
    total_array = len(laser_raw)+1 #count the total amount of ranges
    angle_segment = msg.angle_increment #this is the angle between each range

    half_total_array = total_array/2 #in order to get the middle range
    index_value = index_min - half_total_array
    angle_to_object = angle_segment*(index_value) # to check the angle between range 0 and the middle one

    min_range = min(laser_raw) #the minimum value between car and the object
    extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
    extra_y = math.cos(angle_to_object)*min_range


    if index_value > 0:
        object_position_x = math.floor(x-extra_x)
        object_position_y = math.ceil(y+extra_y)
    else: 
        object_position_x = math.floor(x+extra_x)
        object_position_y = math.ceil(y+extra_y)

    print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." % (curr_pose[0],curr_pose[1]))
    print(x, y)
    print(total_array)
    print(index_value)
    print(index_min)
    print(extra_x, extra_y)
    print(object_position_x,object_position_y) 
    print(min_range)
    print(object_position_x-x)
    print(object_position_y-y)
    #print(msg.ranges)
    print(msg.ranges)

# get the odometry messages
def callback_odom1(msg):
    global curr_pose,curr_ori
 
    pose = msg.pose.pose # has position and orientation
    curr_pose = [float(pose.position.x),float(pose.position.y),float(pose.position.z)]
    curr_ori = [float(pose.orientation.x),float(pose.orientation.y),float(pose.orientation.z),float(pose.orientation.w)]
 

def callback_semcam(msg):
    
    try:
        d = json.loads(msg.data)
        sensor_x = d[0]['position'][0]
        sensor_y = d[0]['position'][1]
        sensor_z = d[0]['position'][2]
        object1 = d[0]['name']
            
    except IndexError:
        sensor_x = 0.0
        sensor_y = 0.0
        sensor_z = 0.0
        object1 = 'Nothing'
    time.sleep(0.2)
    #print ("x: %.2f, y: %.2f, z: %.2f, object: %s." % (sensor_x, sensor_y, sensor_z, object1))
     
if __name__=='__main__':
 
    rospy.init_node("obstacle_check_node")
    rospy.Subscriber('/scan', LaserScan, callback_laser)
    rospy.Subscriber('/camera', String, callback_semcam)
    rospy.Subscriber('/odom', Odometry, callback_odom1) 
    rospy.Subscriber("/pose", PoseStamped, newOdom)
 
    rospy.spin() # this will block untill you hit Ctrl+C
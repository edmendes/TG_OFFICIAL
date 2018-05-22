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

x = 0.0; y = 0.0; heading_angle = 0.0
sensor_x = 0.0; sensor_y = 0.0; sensor_z = 0.0; object1 = 'Nothing'
num1 = 0.0; old_position_x =0.0; old_position_y = 0.0; direction_factor = 0.0


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

def newOdom1(msg):
    global curr_pose
    global theta1

    pose = msg.pose.pose
    curr_pose = [float(pose.position.x),float(pose.position.y),float(pose.position.z)]
  
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler1 = euler_from_quaternion(quaternion)
    roll1 = euler1[0]
    pitch1 = euler1[1]
    theta1 = euler1[2]

def callback_semcam(msg):
    global sensor_x
    global sensor_y
    global sensor_z
    global object1

    #while True:
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

    #sensor_all = [sensor_x, sensor_y, sensor_z]
    """print ("x: %.2f, y: %.2f, z: %.2f, object: %s." % (sensor_x, sensor_y, sensor_z, object1))
    print(sensor_x)"""
    
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

    """print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." %(x,y))
    print(x, y)
    print(total_array)
    print(index_value)
    print(index_min)
    print(extra_x, extra_y)
    print(object_position_x,object_position_y) 
    print(min_range)
    print(object_position_x-x)
    print(object_position_y-y)
    print(msg.ranges)"""

def direction(): 
    global num1
    global old_position_x
    global old_position_y 
    global direction_factor

    """Old_positions keep the variable with a freeze value for 0.4 seconds due to 
    time.sleep function. DeltaX or Y represents the current position minus the 
    old position which was freezed some seconds ago. According with this value, it is
    possible to check what direction the car is going."""

    if (num1 < 2):
        old_position_x = x
        old_position_y = y
        time.sleep(0.1)
        #print("This is x: %.2f and this is y: %.2f" %(old_position_x,old_position_y))
        num1 = num1 + 1

    elif (num1 >= 2 and num1 <= 4):
        time.sleep(0.1)
        num1 = num1 + 1

    else:
        deltaX =  x - old_position_x 
        deltaY = y - old_position_y
        """print("This is x2: %.4f and this is x1: %.4f,DeltaX: %.4f" %(x, old_position_x,deltaX))
        print("This is y2: %.4f and this is y1: %.4f, DeltaY: %.4f " %(y, old_position_y, deltaY))"""
        num1 = 0

        if (deltaX > - 0.2 and deltaX < 0.2 and deltaY > 0.2):
            print("Going North")
            direction_factor = 1
        elif(deltaX > 0.2 and deltaY < 0.2):
            print("Going East")
            direction_factor = 2
        elif(deltaX < -0.2 and deltaY > - 0.2 and deltaY < 0.2):
            print("Going West")
            direction_factor = 3
        elif(deltaX > - 0.2 and deltaX < 0.2 and deltaY < - 0.2):
            print("Going South")
            direction_factor = 4
        else :
            print("Wait")

    return direction_factor    

    print(num1)

rospy.init_node("speed_controller")
rospy.Subscriber('/scan', LaserScan, callback_laser)
rospy.Subscriber('/camera', String, callback_semcam)
rospy.Subscriber('/odom', Odometry, newOdom1) 
rospy.Subscriber("/pose", PoseStamped, newOdom)

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)


while not rospy.is_shutdown():

    direction()

rospy.spin() # this will block untill you hit Ctrl+C  

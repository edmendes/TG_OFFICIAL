#!/usr/bin/env python

import rospy
import json
import numpy as np
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point,Twist,PoseStamped
from math import atan2

x = 0.0
y = 0.0
theta = 0.0
x1 = 0.0
y1 = 0.0
theta1 = 0.0
sensor_x = 0.0
sensor_y = 0.0
sensor_z = 0.0
x_t =0.0
y_t =0.0

def newOdom1(msg):
    global x1
    global y1
    global theta1

    x1 = msg.pose.pose.position.x
    y1 = msg.pose.pose.position.y
    
    
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler1 = euler_from_quaternion(quaternion)
    roll1 = euler1[0]
    pitch1 = euler1[1]
    theta1 = euler1[2]

    

def newOdom(msg):
    global x
    global y
    global theta

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
    theta = euler[2]

    
    

def callback_semcam(msg):
    global sensor_x
    global sensor_y
    global sensor_z
    global object1

    d = json.loads(msg.data)
    sensor_x = d[0]['position'][0]
    sensor_y = d[0]['position'][1]
    sensor_z = d[0]['position'][2]
    object1 = d[0]['name']

    #sensor_all = [sensor_x, sensor_y, sensor_z]
    #print ("x: %.2f, y: %.2f, z: %.2f, object: %s." % (sensor_x, sensor_y, sensor_z, object1))
    #print(sensor_x) 

rospy.init_node("speed_controller")
sub1 = rospy.Subscriber('/camera', String, callback_semcam)
sub2 = rospy.Subscriber("/pose", PoseStamped, newOdom)
sube = rospy.Subscriber("/odom", Odometry, newOdom1)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)

goal = Point()
goal.x = 15
goal.y = 30

while not rospy.is_shutdown():
    inc_x = x_t - x
    inc_y = y_t - y

    angle_to_goal = atan2(inc_y, inc_x)

    diff = sensor_y - y
    
    #the 1 avoids the atrv to start rotating
    if abs(diff) < 10 and abs(diff) > 1:
        if abs(angle_to_goal - theta) > 0.1:
            x_t = x1+5
            y_t = y1+5            
            speed.linear.x = 0.0
            speed.angular.z = 0.3
        else: 
            speed.linear.x = 0.5
            speed.angular.z = 0.0
    else:
        speed.linear.x = 1
    
    pub.publish(speed)
    r.sleep()


    print(theta1)
    print('a')
    print(theta)
    print('b')
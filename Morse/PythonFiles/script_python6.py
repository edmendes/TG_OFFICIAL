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

x = 0.0; y = 0.0; heading_angle = 0.0
x1 = 0.0; y1 = 0.0; theta1 = 0.0
sensor_x = 0.0; sensor_y = 0.0; sensor_z = 0.0; object1 = 'Nothing'
x_t =0.0; y_t =0.0


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
    #print ("x: %.2f, y: %.2f, z: %.2f, object: %s." % (sensor_x, sensor_y, sensor_z, object1))
    #print(sensor_x) 

rospy.init_node("speed_controller")
sub1 = rospy.Subscriber('/camera', String, callback_semcam)
sub2 = rospy.Subscriber("/pose", PoseStamped, newOdom)
sube = rospy.Subscriber("/odom", Odometry, newOdom1)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)

""" goal = Point()
goal.x = 15
goal.y = 30 """

while not rospy.is_shutdown():
    #x and y are the current position in the world, independent of the start
    inc_x = x_t - x
    inc_y = y_t - y
    j=0

    bearing_angle = atan2(inc_y, inc_x)

    diff = sensor_y - y
    
    #the 1 avoids the atrv to start rotating
    if abs(diff) > 1 and abs(diff) < 10 and object1 == 'table':
        #heading_angle is related to the current angle of the car base at the start

        if abs(abs(bearing_angle) - abs(heading_angle)) > 0.1:
             
            while (j<1): 
                x_t = x1+5
                y_t = y1+5
                j=1
            speed.linear.x = 1
            speed.angular.z = 0.3
            print('a')
            
        else: 
            speed.linear.x = 0.3
            speed.angular.z = 0.0
            j=0
            print('b')
    else:
        speed.linear.x = 1
        speed.angular.z= 0
        print('c')
    
    pub.publish(speed)
    r.sleep()
    print(bearing_angle)
    print(heading_angle)
    print(bearing_angle - heading_angle)
    print(object1)
    print(diff)

        
    
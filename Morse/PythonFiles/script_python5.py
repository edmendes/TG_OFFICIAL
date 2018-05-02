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
sensor_x = 0.0
sensor_y = 0.0
sensor_z = 0.0

def newOdom1(msg):
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

    #print(theta)

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
#sub = rospy.Subscriber("/odom", Odometry, newOdom)
sub1 = rospy.Subscriber('/camera', String, callback_semcam)
sub2 = rospy.Subscriber("/pose", PoseStamped, newOdom1)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)
goal = Point()

while not rospy.is_shutdown():

    diff = abs(sensor_y) - abs(y)

    if abs(diff) < 10:
        speed.linear.x = 0.0
    
    else:
        speed.linear.x = .5
    
    pub.publish(speed)
    r.sleep()
    print(sensor_y)
    print(y)

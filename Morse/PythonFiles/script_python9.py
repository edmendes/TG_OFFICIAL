#!/usr/bin/env python

import rospy
import json
import time
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
ref2 = 0
num1 = 0.0; old_position_x =0.0; old_position_y = 0.0; direction_factor = 0.0

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
    print ("x: %.2f, y: %.2f, z: %.2f, object: %s." % (sensor_x, sensor_y, sensor_z, object1))
    print(sensor_x)

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

    #print(num1)
   
def turning_around():
    global x_t
    global y_t
    global ref2

    #x and y are the current position in the world, independent of the start
    inc_x = x_t - x
    inc_y = y_t - y
    ref1=0
    
    bearing_angle = atan2(inc_y, inc_x)

    diff = sensor_y - y # returns the distance between the car and the object
    
    #when ref2 is equal to zero, the program will check if there is some table next to the car
    #However, when ref2 is different, the car is already turning left or right, and no matter if there is
    #a table or not. For this reason, the program goes to "else" and just check heading and bearing angle,
    #and keep the process of turning left or right
    
    if (ref2 ==0):

        if abs(diff) > 1 and abs(diff) < 15 and object1 <> "Nothing":
            #heading_angle is related to the current angle of the car based at the start

            if abs(abs(bearing_angle) - abs(heading_angle)) > 0.05:
                
                while (ref1<1): 
                    x_t = x+1000  #x_t and y_t are responsible to give the bearing angle through atan.
                    y_t = y+10 #example: if x_t << 0 and y_t = 0 (or next to zero) the bearing angle will be pi
                    ref1=1    #ref1 is responsible to keep x_t and y_t with a unique value.                  
                speed.linear.x = 1
                speed.angular.z = -0.3 #angular velocity: negative -> clockwise, positive ->anticlockwise
                ref2 = 1 
                #print('a')
                
            else: 
                speed.linear.x = 0.3
                speed.angular.z = 0.0
                
                #print('b')
        else:
            speed.linear.x = 1
            speed.angular.z= 0
            #print('c')
    
    else:
        if abs(bearing_angle- heading_angle) > 0.1:
                
            speed.linear.x = 1
            speed.angular.z = -0.3
            #print('a1')
          
                
        else: 
            speed.linear.x = 0.3
            speed.angular.z = 0.0
            j=0
            ref2=0
            #print('b1')
    
    pub.publish(speed)
    r.sleep()   
    

rospy.init_node("speed_controller")
sub1 = rospy.Subscriber('/camera', String, callback_semcam)
sub2 = rospy.Subscriber("/pose", PoseStamped, newOdom)
sube = rospy.Subscriber("/odom", Odometry, newOdom1)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)

while not rospy.is_shutdown():
    

    direction() #calling the function to know where the car is going

    turning_around()

    """print(bearing_angle)
    print(heading_angle)
    print(abs(bearing_angle - heading_angle))
    print(object1)
    print(diff)
    print(ref2)"""

        
    
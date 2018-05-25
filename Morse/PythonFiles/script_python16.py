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

x = 0.0; y = 0.0; heading_angle = 0.0
curr_pose = (0,0)
sensor_x = 0.0; sensor_y = 0.0; sensor_z = 0.0; object1 = 'Nothing'
min_range = 0.0; angle_to_object =0.0; index_value =0.0
num2= 0.0; lateral_laser = 0.0; laser_x1 =0.0; laser_x2 =0.0; lateral_laser_max = 0.0
num1 = 0.0; old_position_x =0.0; old_position_y = 0.0; direction_factor = 0.0; deltaX =0.0; deltaY =0.0
object_position_x = 0.0; object_position_y =0.0; buffer = 0.0
bearing_angle = 0; ref2 = 0; diffx = 0.0; diffy = 0.0
previousError = 0; Integral = 0


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
    global angle_to_object
    global min_range
    global index_value

    angle_segment = 0

    laser_raw = msg.ranges #a group of multiple vectors which contains the distance between the car and an object
    index_min = min(xrange(len(laser_raw)), key=laser_raw.__getitem__) #get the vector number which contains the minimum value of the range mentioned above
    
    total_array = len(laser_raw)+1 #count the total amount of ranges
    angle_segment = msg.angle_increment #this is the angle between each range

    half_total_array = total_array/2 #in order to get the middle range
    index_value = index_min - half_total_array
    angle_to_object = angle_segment*(index_value) # to check the angle between range 0 and the middle one

    min_range = min(laser_raw) #the minimum value between car and the object
    
    """print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." %(x,y))
    #print(x, y)
    #print(total_array)
    #print(index_value)
    #print(index_min)
    print(extra_x, extra_y)
    print(object_position_x,object_position_y) 
    #print(min_range)
    print(object_position_x-x)
    print(object_position_y-y)
    #print(msg.ranges
    return angle_to_object, min_range"""

def callback_laser1(msg):
    global lateral_laser, lateral_laser_max

    index_min = min(xrange(len(msg.ranges)), key=msg.ranges.__getitem__) #get the vector number which contains the minimum value of the range mentioned above
    index_max = max(xrange(len(msg.ranges)), key=msg.ranges.__getitem__) 
    lateral_laser= msg.ranges[index_min]
    lateral_laser_max = msg.ranges[index_max]
    
    #print(lateral_laser)
   
def direction(): 
    global num1
    global old_position_x, old_position_y
    global deltaX, deltaY
    global direction_factor

    #Old_positions keep the variable with a freeze value for 0.4 seconds due to 
    #time.sleep function. DeltaX or Y represents the current position minus the 
    #old position which was freezed some seconds ago. According with this value, it is
    #possible to check what direction the car is going.

    if (num1 < 2):
        old_position_x = x
        old_position_y = y
        time.sleep(0.01)
        #print("This is x: %.2f and this is y: %.2f" %(old_position_x,old_position_y))
        num1 = num1 + 1

    elif (num1 >= 2 and num1 <= 4):
        time.sleep(0.01)
        num1 = num1 + 1

    else:
        deltaX =  x - old_position_x #deltaX is the x position difference between present and a moment 0.05s ago 
        deltaY = y - old_position_y #deltaY is the y position difference between present and a moment 0.05s ago
        #print("This is x2: %.4f and this is x1: %.4f,DeltaX: %.4f" %(x, old_position_x,deltaX))
        #print("This is y2: %.4f and this is y1: %.4f, DeltaY: %.4f " %(y, old_position_y, deltaY))
        num1 = 0

        if (deltaX > - 0.05 and deltaX < 0.05 and deltaY > 0.05): #in this case x do not change too much and y is increasing faster which indicates that the car is going to North
            direction_factor = 1
        elif(deltaX > 0.05  and deltaY> -0.05 and  deltaY < 0.05):#in this case y do not change too much and x is increasing faster which indicates that the car is going to East
            direction_factor = 2
        elif(deltaX > - 0.05  and deltaX < 0.05  and deltaY < - 0.05 ): #in this case x do not change too much and y is decreasing faster which indicates that the car is going to South
            direction_factor = 3
        elif(deltaX < -0.05  and deltaY > - 0.05 and deltaY < 0.05 ): #in this case y do not change too much and x is decreasing faster which indicates that the car is going North
            direction_factor = 4
        else :
            direction_factor = 5 #an exception to all those cases

    return direction_factor, deltaX, deltaY    

def object_scenary_position(index_value, angle_to_object, min_range, direction_factor):
    global object_position_x 
    global object_position_y
    global buffer  #in order to keep the last state of movement

    if direction_factor == 1:
        extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.cos(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.ceil(y+extra_y)
        else: 
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.ceil(y+extra_y)

        buffer = direction_factor

    elif direction_factor == 2:
        extra_x = math.cos(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.sin(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.ceil(y+extra_y)
        else: 
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.floor(y-extra_y)
        
        buffer = direction_factor

    elif direction_factor == 3:
        extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.cos(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.floor(y-extra_y)
        else: 
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.floor(y-extra_y)
        
        buffer = direction_factor
    
    elif direction_factor == 4:
        extra_x = math.cos(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.sin(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.floor(y-extra_y)
        else: 
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.ceil(y+extra_y)

        buffer = direction_factor
    else:
        extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.cos(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = 10000
            object_position_y = 10000
        else: 
            object_position_x = 10000
            object_position_y = 10000

    distance_between_objects_x = object_position_x-x
    distance_between_objects_y = object_position_y-y

    """print(extra_x, extra_y)"""
    #print(object_position_x,object_position_y)
    """print(distance_between_objects_x)
    print(distance_between_objects_y)"""

    return distance_between_objects_x, distance_between_objects_y, buffer

def turning_around(distance_between_objects_x, distance_between_objects_y,buffer):
    #buffer: 1 - North, 2 - East, 3 - South, 4 -West
    global bearing_angle
    global ref2
    global diffx, diffy
    print("aaaaaaaaaaaaaaaaaaaaaaaaS")
    turn_choose = 1 #zero indicates that the car intend to turn left, 1 turn right
    
    if ref2 < 1: #ref2 is responsile to keep the diffx and diffy the same until complete the turning process
        diffx = abs(distance_between_objects_x) # returns the distance between the car and the object
        diffy = abs(distance_between_objects_y)
    else:
        diffy = diffy
        diffx = diffx

    angle_objective = abs(bearing_angle - heading_angle)

   
    if(buffer==1 and turn_choose==0 and diffy < 12): #Going North, Turn Right, DeltaY between object and car is 12
        ref2 = 1    #started process of turning around
        bearing_angle = math.pi #in this case heading angle is pi/2. Thus, to go to West, it needs to turn right til reach pi.

        if abs(angle_objective) > 0.1: #Turning Right until bearing angle-heading angle be less than 0.1
            print("Xo1")
            speed.linear.x = 1
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)
    
    elif(buffer==1 and turn_choose==1 and diffy < 12): #Going North, Turn Left, DeltaY between object and car is 12
        ref2 = 1
        bearing_angle = 0

        if abs(angle_objective) > 0.1:
            print("Xo1")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(buffer==2 and turn_choose==0 and diffx < 12): #Going East, Turn Right, DeltaY between object and car is 12   
        ref2 = 1
        bearing_angle = math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo2")
            speed.linear.x = 1
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(buffer==2 and turn_choose==1 and diffx < 12): #Going East, Turn Left, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = -math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo2")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)
    
    elif(buffer==3 and turn_choose==0 and diffy < 12): #Going South, Turn Right, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = 0

        if abs(angle_objective) > 0.1:
            print("Xo3")
            speed.linear.x = 1
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(buffer==3 and turn_choose==1 and diffy < 12): #Going South, Turn Left, DeltaY between object and car is 12   
        ref2 = 1
        bearing_angle = -math.pi

        if abs(angle_objective) > 0.1:
            print("Xo3")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(buffer==4 and turn_choose==0 and diffx < 12): #Going West, Turn Right, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = -math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo4")
            speed.linear.x = 1
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(buffer==4 and turn_choose==1 and diffx < 12): #Going West, Turn Left, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo4")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)
    else:
        speed.linear.x = 1
        speed.angular.z = 0
    
    """print(buffer) #the last direction value , North, East, South, West
    #print(turn_choose) #0 Turn Left, 1 Turn Right
    print(diffy) #Distance Between Object and the car
    print(diffx)
    print(angle_objective) #Angle that a want to reach
    print(bearing_angle)
    print(heading_angle)"""
    print("a")

    pub.publish(speed)
    r.sleep()   
    
def PID(wanted_value, current_value):
    global previousError, Integral
    Kp = 0.5
    Ki = 0.001
    Kd = 0.05
    

    error = wanted_value - current_value
    Proportional = error
    Integral = Integral + error
    Differential = error - previousError

    PIDvalue = (Kp*Proportional) + (Ki*Integral) + (Kd*Differential)
    """print("Error: %.7f" %error)
    print("Proportional: %.7f" %Proportional)
    print("Integral: %.7f" %Integral)
    print("Differential: %.7f" %Differential)"""
    previousError = abs(error) - abs(previousError)

    return PIDvalue

def detecting_sidewalk(lateral_laser, lateral_laser_max, i1, i2, i3 ):
    global num2, laser_x1, laser_x2

    
    if num2 < 1:
        laser_x1 = lateral_laser
        #time.sleep(0.1)
        num2 = num2 +1

    elif num2 == 1:
        laser_x2 = lateral_laser - laser_x1
        num2 = 0

    #diff_lateral_laser = lateral_laser_max - lateral_laser    
    print("Lateral laser %.5f" %lateral_laser)
    print("Lateral Max %.5f" %lateral_laser_max)
    """print(laser_x1)
    print(laser_x2)"""

    if lateral_laser_max < 4.9:
        if heading_angle > (-math.pi/2-0.75) and heading_angle <  (-math.pi/2+0.75):
            ast = -math.pi/2
        elif heading_angle > (-0.75) and heading_angle < (0.75):
            ast = 0
        elif heading_angle > (math.pi/2-0.75) and heading_angle <  (math.pi/2+0.75):
            ast = math.pi/2
        elif heading_angle > (math.pi -0.75) and heading_angle < (math.pi+0.75) :
            ast = math.pi
        else:
            ast = -math.pi

        pid_angle = PID(ast, heading_angle)
        pid_straight_line = PID(2, lateral_laser)

        if lateral_laser < 1.90 or (lateral_laser > 2.1 and lateral_laser <4.5):
            speed.linear.x = 1 + pid_angle
            speed.angular.z = pid_angle - pid_straight_line
        
        elif lateral_laser > 4.5:
            speed.linear.x = 0
            speed.angular.z = 0
        
        else:  #final adjustments
            if laser_x2 < -0.001:
                speed.linear.x = 1
                speed.angular.z = -0.02

            elif laser_x2 > 0.001:
                speed.linear.x = 1
                speed.angular.z = 0.02
            
            else: 
                speed.linear.x = 1
                speed.angular.z = 0.00

        """print("pid_angle: %.5f"%pid_angle)
        print("pid_straight_line: %.5f"%pid_straight_line)
        print(speed.angular.z)"""

    else: 
        turning_around(i1, i2, i3)
    
  

    pub.publish(speed)
    r.sleep() 

rospy.init_node("speed_controller")
rospy.Subscriber('/scan', LaserScan, callback_laser)
rospy.Subscriber('/scan1', LaserScan, callback_laser1)
rospy.Subscriber('/camera', String, callback_semcam)
rospy.Subscriber('/odom', Odometry, newOdom1) 
rospy.Subscriber("/pose", PoseStamped, newOdom)

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)


while not rospy.is_shutdown():

    z1, z2, z3 = direction()

    i1, i2, i3 = object_scenary_position(index_value, angle_to_object,min_range, z1)

    detecting_sidewalk(lateral_laser, lateral_laser_max, i1, i2, i3)


    if direction_factor == 1:
        print("Going North")
    elif direction_factor == 2:
        print("Going East")
    elif direction_factor == 3:
        print("Going South")
    elif direction_factor == 4:
        print("Going West")
    elif direction_factor == 5:
        print("Wait")
    else:
        print("Error")
    
    #print(z2, z3)
    #print(i3)
rospy.spin() # this will block untill you hit Ctrl+C  

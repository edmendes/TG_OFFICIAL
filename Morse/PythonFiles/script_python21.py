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

x = 0.0; y = 0.0; z=0.0; heading_angle = 0.0
sensor_x = 0.0; sensor_y = 0.0; sensor_z = 0.0; object1 = 'Nothing'
min_range = 0.0; angle_to_object =0.0; index_value =0.0

num2= 0.0; lateral_laser = 0.0; laser_x1 =0.0; laser_x2 =0.0; lateral_laser_max = 0.0; desired_angle=0
num1 = 0.0; old_position_x =0.0; old_position_y = 0.0; direction_factor = 0.0; deltaX =0.0; deltaY =0.0
object_position_x = 0.0; object_position_y =0.0; wind_rose = 0.0
bearing_angle = 0; ref2 = 0; diffx = 0.0; diffy = 0.0
previousError = 0; Integral = 0
final_choice = 100


# get the laser messages
def newOdom(msg):
    global x
    global y
    global z
    global heading_angle

    x = msg.pose.position.x
    y = msg.pose.position.y
    z = msg.pose.position.z

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
    global angle_to_object
    global min_range
    global index_value

    angle_segment = 0

    laser_raw = msg.ranges #a group of multiple vectors which contains the distance between the car and an object
    index_min = min(xrange(len(laser_raw)), key=laser_raw.__getitem__) #get the vector number which contains the minimum value of the range mentioned above
    
    total_array = len(laser_raw)+1 #count the total amount of vectors 
    angle_segment = msg.angle_increment #this is the angle between each vector

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

    tolerance_angle = 0.2

    #Old_positions keep the variable with a freeze value for 0.4 seconds due to 
    #time.sleep function. DeltaX or Y represents the current position minus the 
    #old position which was freezed some seconds ago. According with this value, it is
    #possible to check what direction the car is going.


    if (num1 < 2): #the num1 is a wind_rose, the value of x and y should be stored for 0.03s to compare to a current value.
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

    return direction_factor, deltaX, deltaY    

def object_scenary_position(index_value, angle_to_object, min_range, direction_factor):
    global object_position_x 
    global object_position_y
    global wind_rose  #in order to keep the last state of movement

    if direction_factor == 1:
        extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.cos(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.ceil(y+extra_y)
        else: 
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.ceil(y+extra_y)

        wind_rose = direction_factor

    elif direction_factor == 2:
        extra_x = math.cos(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.sin(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.ceil(y+extra_y)
        else: 
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.floor(y-extra_y)
        
        wind_rose = direction_factor

    elif direction_factor == 3:
        extra_x = math.sin(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.cos(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.ceil(x+extra_x)
            object_position_y = math.floor(y-extra_y)
        else: 
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.floor(y-extra_y)
        
        wind_rose = direction_factor
    
    elif direction_factor == 4:
        extra_x = math.cos(angle_to_object)*min_range #it is the value of x which must be add or withdraw to pretend the object position
        extra_y = math.sin(angle_to_object)*min_range

        if index_value > 0:
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.floor(y-extra_y)
        else: 
            object_position_x = math.floor(x-extra_x)
            object_position_y = math.ceil(y+extra_y)

        wind_rose = direction_factor
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

    return distance_between_objects_x, distance_between_objects_y, wind_rose

def turning_around(distance_between_objects_x, distance_between_objects_y,wind_rose, choice):
    
    #wind_rose: 1 - North, 2 - East, 3 - South, 4 -West
    global bearing_angle #it is the angle which needed to make the car be directed to the objective, for example to North for West the desired angle is math.pi()
    global ref2 #responsible to check if the car is going straight or curve
    global diffx, diffy #it is the abs value of distance between car and object. 
    print("Initiating the turning left or right movement...")
    turn_choose = choice #zero indicates that the car intend to turn left, 1 turn right and 2 move ahead. 
    
    if ref2 < 1: #ref2 is responsile to keep the diffx and diffy the same until complete the turning process
        diffx = abs(distance_between_objects_x) # returns the distance between the car and the object
        diffy = abs(distance_between_objects_y)
    else:
        diffy = diffy
        diffx = diffx

    angle_objective = abs(bearing_angle - heading_angle)

   
    if(wind_rose==1 and turn_choose==0 and diffy < 12): #Going North, Turn Right, DeltaY between object and car is 12
        ref2 = 1    #started process of turning around
        bearing_angle = math.pi #in this case heading angle is pi/2. Thus, to go to West, it needs to turn right til reach pi.

        if abs(angle_objective) > 0.1: #Turning Right until bearing angle-heading angle be less than 0.1
            print("Xo1")
            speed.linear.x = 1.2
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1) #not sure if it is necessary
    
    elif(wind_rose==1 and turn_choose==1 and diffy < 12): #Going North, Turn Left, DeltaY between object and car is 12
        ref2 = 1
        bearing_angle = 0

        if abs(angle_objective) > 0.1:
            print("Xo1")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(wind_rose==2 and turn_choose==0 and diffx < 12): #Going East, Turn Right, DeltaY between object and car is 12   
        ref2 = 1
        bearing_angle = math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo2")
            speed.linear.x = 1.2
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(wind_rose==2 and turn_choose==1 and diffx < 12): #Going East, Turn Left, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = -math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo2")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)
    
    elif(wind_rose==3 and turn_choose==0 and diffy < 12): #Going South, Turn Right, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = 0

        if abs(angle_objective) > 0.1:
            print("Xo3")
            speed.linear.x = 1.2
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(wind_rose==3 and turn_choose==1 and diffy < 12): #Going South, Turn Left, DeltaY between object and car is 12   
        ref2 = 1
        bearing_angle = -math.pi

        if abs(angle_objective) > 0.1:
            print("Xo3")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(wind_rose==4 and turn_choose==0 and diffx < 12): #Going West, Turn Right, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = -math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo4")
            speed.linear.x = 1.2
            speed.angular.z = 0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif(wind_rose==4 and turn_choose==1 and diffx < 12): #Going West, Turn Left, DeltaY between object and car is 12    
        ref2 = 1
        bearing_angle = math.pi/2

        if abs(angle_objective) > 0.1:
            print("Xo4")
            speed.linear.x = 2
            speed.angular.z = -0.3
        else:
            ref2 = 0
            speed.linear.x = 1.0
            speed.angular.z = 0.0
            print(speed.angular.z)
            time.sleep(0.1)

    elif   (turn_choose==2):
        speed.linear.x = 2
        speed.angular.z = -1

    else:
        speed.linear.x = 1
        speed.angular.z = 0
    
    """print(wind_rose) #the last direction value , North, East, South, West
    #print(turn_choose) #0 Turn Left, 1 Turn Right
    print(diffy) #Distance Between Object and the car
    print(diffx)
    print(angle_objective) #Angle that a want to reach
    print(bearing_angle)
    print(heading_angle)"""
    print("a")

    pub.publish(speed)
    r.sleep()   


def wind_rose_function(wind_rose, objective_wind_rose):

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
        final_choice = 100

    return final_choice

def PID(wanted_value, current_value):
    global previousError, Integral
    Kp = 0.5 #this constants were attributed based on tests. 
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

def detecting_sidewalk(lateral_laser, lateral_laser_max, i1, i2, i3, turn_choice):
    global num2, laser_x1, laser_x2, desired_angle

    if turn_choice == 0: #this was used to give the curve moment a smoothly movement
        minimum_laser_difference = 2
        laser_max_option = 5
    
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
    print("Lateral Max %.5f" %lateral_laser_max)
    """print(laser_x1)
    print(laser_x2)"""

    if lateral_laser_max <= laser_max_option and laser_x2 < minimum_laser_difference: #if the car follow these statements it should go straight or should correct it movement to go straight
        if heading_angle > (-math.pi/2-0.75) and heading_angle < (-math.pi/2+0.75): #if the heading angle is between this values, the car is going West, so the heading angle must be directed to -pi/2
            desired_angle = -math.pi/2
        elif heading_angle > (-0.75) and heading_angle < (0.75):
            desired_angle = 0
        elif heading_angle > (math.pi/2-0.75) and heading_angle < (math.pi/2+0.75):
            desired_angle = math.pi/2
        elif heading_angle > (math.pi -0.75) and heading_angle < (math.pi+0.75) :
            desired_angle = math.pi
        elif heading_angle >= (-math.pi) and heading_angle <(-math.pi + 0.75):
            desired_angle = -math.pi
        else:
            desired_angle = desired_angle


        print(desired_angle)

        pid_angle = PID(desired_angle, heading_angle) #controller to keep the car near to the desired angle
        pid_straight_line = PID(2, lateral_laser) #contoreller to keep the car in a proper distance to the sidewalk

        if lateral_laser < 1.90 or (lateral_laser > 2.1 and lateral_laser < 4.5):
            speed.linear.x = 1 + pid_angle - pid_straight_line
            speed.angular.z = pid_angle - pid_straight_line 
        
        elif lateral_laser > 5.0:
            speed.linear.x = 0
            speed.angular.z = 0
        
        else:  #final adjustments, when the car is almost riding straigh it keeps it going straight
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

        print(speed.linear.x)
        print(speed.angular.z)

    else: 
        turning_around(i1, i2, i3, turn_choice)
    
  

    pub.publish(speed)
    r.sleep() 

rospy.init_node("speed_controller")
rospy.Subscriber('/scan', LaserScan, callback_laser)
rospy.Subscriber('/scan1', LaserScan, callback_laser1)
rospy.Subscriber("/pose", PoseStamped, newOdom)

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)


while not rospy.is_shutdown():

    z1, z2, z3 = direction()

    i1, i2, i3 = object_scenary_position(index_value, angle_to_object,min_range, z1)

    final_choice =  wind_rose_function(wind_rose, 4)
    
    detecting_sidewalk(lateral_laser, lateral_laser_max, i1, i2, i3, final_choice) #the last statement indicates if is turning left - 0 or right - 1, go back -2 or go ahead - 3 and also keeping the movement


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

    print(z)
    if z < -10:
        rospy.signal_shutdown('I want')
        
    
    #print(z2, z3)
    #print(i3)
rospy.spin() # this will block untill you hit Ctrl+C  

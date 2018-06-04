#!/usr/bin/env python

import rospy
import json
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import numpy as np
 
# get the laser messages
def callback_laser(msg):
    global curr_pose
    laser_raw = msg.ranges
    laser_float = [float(r) for r in laser_raw]
 
    if np.min(laser_float)<1.5:
        print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." % (curr_pose[0],curr_pose[1]))
  
# get the odometry messages
def callback_odom(msg):
    global curr_pose,curr_ori
 
    pose = msg.pose.pose # has position and orientation
    curr_pose = [float(pose.position.x),float(pose.position.y),float(pose.position.z)]
    curr_ori = [float(pose.orientation.x),float(pose.orientation.y),float(pose.orientation.z),float(pose.orientation.w)]
 

def callback(msg):
    position = msg.pose.position
    curr_pose1 =  [position.x , position.y, position.z]

    print curr_pose1[0]


def callback_semcam(msg):

    d = json.loads(msg.data)
    sensor_x = d[0]['position'][0]
    sensor_y = d[0]['position'][1]
    sensor_z = d[0]['position'][2]
    object1 = d[0]['name']

    sensor_all = [sensor_x, sensor_y, sensor_z]

    #print ("x: %.2f, y: %.2f, z: %.2f, object: %s." % (sensor_x, sensor_y, sensor_z, object1))
def main():

    print 1

if __name__=='__main__':
 
    rospy.init_node("obstacle_check_node")
    rospy.Subscriber('/scan', LaserScan, callback_laser)
    rospy.Subscriber('/camera', String, callback_semcam)
    rospy.Subscriber('/odom', Odometry, callback_odom) 
    rospy.Subscriber("/pose", PoseStamped, callback)
    main()
    rospy.spin() # this will block untill you hit Ctrl+C


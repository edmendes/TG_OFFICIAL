#!/usr/bin/env python
 
import rospy
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud2
from nav_msgs.msg import Odometry
import numpy as np
 
# get the laser messages
def callback_laser(msg):
    global curr_pose
    laser_raw = msg.ranges
    laser_float = [float(r) for r in laser_raw]
 
<<<<<<< HEAD:Morse/PythonFiles/script_python.py
    if np.min(laser_float)<0.5:
        print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." % (curr_pose[0],curr_pose[1]))
=======
    if np.min(laser_float)<5.0:
        print "I bumped at (X:%.2f Y:%.2f). Please Reverse."%(curr_pose[0],curr_pose[1])
>>>>>>> d40cd9a15276763b3a0d8182f263e583e33ce2e4:morse_tut/obstacle_check.py
 
# get the odometry messages
def callback_odom(msg):
    global curr_pose,curr_ori
 
    pose = msg.pose.pose # has position and orientation
 
    curr_pose = [float(pose.position.x),float(pose.position.y),float(pose.position.z)]
    curr_ori = [float(pose.orientation.x),float(pose.orientation.y),float(pose.orientation.z),float(pose.orientation.w)]
 
if __name__=='__main__':
 
    rospy.init_node("obstacle_check_node")
    rospy.Subscriber('/scan', LaserScan, callback_laser)
    rospy.Subscriber('/odom', Odometry, callback_odom)
 
    rospy.spin() # this will block untill you hit Ctrl+C
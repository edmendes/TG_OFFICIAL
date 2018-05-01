#!/usr/bin/env python
import rospy
import json
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import numpy as np

class SensorData():
            
    """ 
    ROS class guidance to build this (get euclidean distance): http://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal 
    POO in Python: https://python.swaroopch.com/oop.html
    Accessing attributes in Python: http://blog.thedigitalcatonline.com/blog/2015/01/12/accessing-attributes-in-python/
    """ 
    #The __init__ method defines the object instantiation operation
    def __init__(self):
        
        """
        Instances for each Publisher (ignore this part for a while)
        """
        #self.distance_publisher = rospy.Publisher('dist',std_msgs.msg, queue_size=10)

        """  
        Attributes instances for each Subscriber, corresponding to each ATVR sensor topic
        Only Semantic camera and Pose implemented for a while
        """
        # self.laser_subscriber = rospy.Subscriber('/scan', LaserScan, self.callback_laser)
        # self.odom_subscriber = rospy.Subscriber('/odom', Odometry, callback_odom) 
        self.semcam_subscriber  = rospy.Subscriber('/camera', String, self.callback_semcam)
        self.pose_subcriber = rospy.Subscriber('/pose', PoseStamped, self.callback_pose)

        """  
        Attributes instances for sensors' parameters
        """
        self.pose = PoseStamped() #attribute for PoseStamped method in order to get the initial value for pose (and being synchronized after calling callback_pose)
        # self.odom = Odometry()
        # self.laser = LaserScan()
        self.semcam_position = 0.0 #attribute for the specific float element (position x of passive object) of a list from JSON data returned by Semantic Camera - zero as initial value
        self.rate = rospy.Rate(1) #attribute for Rate in Hz (velocity in which the messages will be received by Subscribers) 

    # get laser messages
    """ def callback_laser(self, msg):
        
        laser_raw = msg.ranges
        laser_float = [float(r) for r in laser_raw]
    
        if np.min(laser_float)<5.0:
            print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." % (curr_pose[0],curr_pose[1])) """

    # get pose messages
    def callback_pose(self, msg):

        self.pose = msg #update pose attribute  with msg returned by sensor
        self.pose.pose.position.x = round(self.pose.pose.position.x, 3) #update pose attribute in pose.position.x returned by msg from sensor - the same of msg.pose.position.x
        self.pose.pose.position.y = round(self.pose.pose.position.y, 3) #update pose attribute in pose.position.y returned by msg from sensor - the same of msg.pose.position.y

    # get semantic camera messages of tagged passive object
    def callback_semcam(self, msg):
        d = json.loads(msg.data)
        #handle "list index out of range" with Python exception, i.e., when the SemanticCamera don't identify a passive object in front of it
        try: 
            self.semcam_position = d[0]['position'][0] #update semcam_position attribute with position 0 of list 0 from JSON data returned by Semantic Camera
        except IndexError:
            self.semcam_position = 0.0 #zero to dont get errors during distance calculation from get_distance() method
        
    
    # get x distance between robot and table (passive object in Blender scene)
    def get_distance(self):
        rospy.loginfo("Ca estoy")
        while not rospy.is_shutdown():
            #rospy.loginfo(self.posex)
            #rospy.loginfo(self.semcam)
            print "robot X position: %s" % self.pose.pose.position.x
            print "table X position: %s" % self.semcam_position
            # print self.pose.pose.position.x
            # print self.pose.pose.position.y
            # print self.semcam_position
            print "distance between X robot and X table: %s" % (self.pose.pose.position.x - self.semcam_position)
            self.rate.sleep()
                
if __name__=='__main__':   
    
    rospy.init_node("obstacle_check_node") #iniciate ROS node
    my_sensor = SensorData() #instance the SensorData class as an object named as my_sensor
    my_sensor.get_distance() #call get_distance() method of my_sensor object

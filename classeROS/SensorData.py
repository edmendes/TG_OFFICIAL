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

    #The _init_ method defines the object instantiation operation
    def __init__(self):

        #instances for each Publisher, corresponding to the each ATVR sensor
        # topics where we publish
        #self.distance_publisher = rospy.Publisher('dist',std_msgs.msg, queue_size=10)

        #subscribed topics
        # self.laser_subscriber = rospy.Subscriber('/scan', LaserScan, self.callback_laser)
        self.semcam_subscriber  = rospy.Subscriber('/camera', String, self.callback_semcam)
        # self.odom_subscriber = rospy.Subscriber('/odom', Odometry, callback_odom) 
        self.pose_subcriber = rospy.Subscriber("/pose", PoseStamped, self.callback_pose)
        

        #instances for sensors' parameters
        self.pose = PoseStamped()
        self.semcam = 0.0
        self.rate = rospy.Rate(1)

    # get laser messages
    def callback_laser(self, msg):
        
        laser_raw = msg.ranges
        laser_float = [float(r) for r in laser_raw]
    
        """ if np.min(laser_float)<5.0:
            print ("I bumped at (X:%.2f Y:%.2f). Please Reverse." % (curr_pose[0],curr_pose[1]))  """
  
    # get pose messages
    def callback_pose(self, msg):
        self.pose = msg
        self.pose.pose.position.x = round(self.pose.pose.position.x, 3)
        self.pose.pose.position.y = round(self.pose.pose.position.y, 3)
    # get semantic camera messages
    def callback_semcam(self, msg):
    
        d = json.loads(msg.data)
        self.semcam = d[0]['position'][0]

    def get_distance(self):
        rospy.loginfo("Ca estoy")
        while not rospy.is_shutdown():
                """ rospy.loginfo(self.posex)
                rospy.loginfo(self.semcam) """
                #print "posicao x do robot: X:%.2f" % float(self.posex)
                print self.pose.pose.position.x 
                print self.semcam
                print self.pose.pose.position.x - self.semcam
                #print self.pose.pose.position.y
                #print "posicao X da mesa: X:%.2f" % float(self.semcam)
                # print round(self.semcam, 4)
                self.rate.sleep()
                

   
if __name__=='__main__':   
    
    rospy.init_node("obstacle_check_node")
    my_sensor = SensorData()
    my_sensor.get_distance()

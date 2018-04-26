#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Twist


cmd = rospy.Publisher("/atrv/motion", Twist, queue_size=10)
motion = Twist()

def callback(msg):
    position = msg.pose.position
    if position.y < 1:
        motion.linear.x = +0.5
    if position.y > 2:
        motion.linear.x = -0.5
    cmd.publish(motion)

def callback_sensor(msg) #continuar daqui

rospy.init_node("rostuto1")
rospy.Subscriber("/atrv/pose", PoseStamped, callback)
rospy.Subscriber("/scan", PointCloud2, callback_sensor)
rospy.spin() # this will block untill you hit Ctrl+C
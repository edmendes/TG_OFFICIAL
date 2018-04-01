#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

cmd = rospy.Publisher("/atrv/motion", Twist, queue_size=10)
motion = Twist()


def callback(msg):
    position = msg.pose.position
    if position.y < 1: 
        motion.linear.x = +0.5
    if position.y > 5:
        motion.linear.x = -0.5
    cmd.publish(motion)



rospy.init_node("rostuto1")
rospy.Subscriber("/atrv/pose", PoseStamped, callback)
rospy.spin() # this will block untill you hit Ctrl+C

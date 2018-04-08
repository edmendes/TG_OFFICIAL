#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

cmd = rospy.Publisher("/atrv/motion", Twist, queue_size=10)
motion = Twist()

def wander(message):
    assert(len(message.ranges) >= 30)
    mid = len(message.ranges) // 2

    # halt if an object is less than 2m in a 30deg angle
    halt = False
    for distance_to_object in message.ranges[mid-15:mid+15]:
        if distance_to_object < 2:
            halt = True
            break
    if halt:
        # we go to the highest-range side scanned
        if sum(message.ranges[:mid]) > sum(message.ranges[mid:]):
            cmd.angular.z = -1
        else:
            cmd.angular.z = +1
    else:
        cmd.linear.x = 1
    # publish twist
    cmd.publish(motion)

def callback(msg):
    position = msg.pose.position
    if position.y < 1: 
        motion.linear.x = +0.5
    if position.y > 5:
        motion.linear.x = -0.5
    cmd.publish(motion)



if __name__ == '__main__':
    # ./nodes/wander.py cmd:=/robot/motion laser:=/robot/sick
    rospy.init_node('wander')
    rospy.loginfo("wander rospy initialized")
    # see: ros.org/doc/api/sensor_msgs/html/msg/LaserScan.html
    rospy.Subscriber('laser', LaserScan, wander)
    rospy.Subscriber("/atrv/pose", PoseStamped, callback)
    rospy.spin() # block while ROS-node is up, Ctrl+C to stop
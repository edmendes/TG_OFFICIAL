import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

cmd = rospy.Publisher("/atrv/motion",  Twist, queue_size=10)
motion = Twist()
def callback(msg):
    cmd.publish("Hello world")

rospy.init_node("rostuto1")
rospy.Subscriber("/atrv/pose", PoseStamped, callback)
rospy.spin() # this will block untill you hit Ctrl+C
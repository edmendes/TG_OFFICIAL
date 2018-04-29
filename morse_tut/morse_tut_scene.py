from morse.builder import *

atrv = ATRV() #the robot
atrv.translate(x=-31, z=-4.9) #starting location
atrv.rotate(z=3.14/2)

#adding a passive object
table = PassiveObject('props/objects','SmallTable')
table.setgraspable()
table.translate(x=-31, y=5, z=-4.9)
table.properties(Type = "table", Object = True, Graspable = True, Label = "TABLE")
 
# Allows to control the robot with the keyboard
keyboard = Keyboard()
atrv.append(keyboard)


"""
SENSORS: odometria, laserscan
"""
# An odometry sensor to get odometry information
odometry = Odometry()
atrv.append(odometry)
odometry.add_interface('ros', topic="/odom",frame_id="odom", child_frame_id="base_link")

pose = Pose()
pose.translate(z=0.83)
atrv.append(pose)
pose.add_interface('ros', topic='/pose')
 
#laser 10Hz, 180 degrees wide with a 180 points
scan = Sick()
scan.translate(x=0.275, z=0.252)
scan.properties(Visible_arc = True,laser_range = 10.0,resolution = 1,scan_window = 180.0)
scan.frequency(5)
scan.create_laser_arc()
scan.add_interface('ros', topic='/scan',frame_id="laser", child_frame_id="base_link")
atrv.append(scan)
 
#motion controller
motion = MotionXYW()
atrv.append(motion)
motion.add_interface('ros', topic='/cmd_vel')
 
# Set the environment
env = Environment('/home/nana/morse-1.3/data/environments/estacionamento/estacionamento')
env.set_camera_location([-25, -7, 2])
env.set_camera_rotation([1.0470, 0, 0.7854])
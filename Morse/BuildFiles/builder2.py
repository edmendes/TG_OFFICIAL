from morse.builder import *
 
atrv = ATRV() #the robot
atrv.translate(x=-31, z=-4.9) #starting location
atrv.rotate(z=3.14/2)

#adding a dumb robot 
atrv1 = ATRV() #the robot
atrv1.translate(x=-25, y=5, z=-4.9) #starting location
atrv1.rotate(z=3.14/2)

#adding a passive object
table = PassiveObject('props/objects','SmallTable')
table.setgraspable()
table.translate(x=-31, y=20, z=-4.9)
#table.rotate(z=0.2)
table.properties(Type = "table", Object = True, Graspable = True, Label = "TABLE")

"""
SENSORS: odometria, camera, laserscan
"""
# An odometry sensor to get odometry information
odometry = Odometry()
atrv.append(odometry)
odometry.add_interface('ros', topic="/odom",frame_id="odom", child_frame_id="base_link")

pose = Pose()
pose.translate(z=0.83)
atrv.append(pose)
pose.add_interface('ros', topic='/pose')
'''
pose.add_stream('ros')'''

camera = SemanticCamera()
atrv.append(camera)
camera.properties(tag = "table")
camera.translate(x=0.3, z=0.762)
camera.add_interface('ros',topic='/camera',frame_id="odom", child_frame_id="base_link")


#camera 10Hz, 320x240 image
"""cam_frequency = 10
camera = VideoCamera()
camera.translate(x = 0.7, z= 0.5)
camera.rotate(y = -0.0)
camera.properties(cam_width=320,cam_height=240,cam_focal=6.,cam_near=0.1,cam_far=500)
camera.frequency(cam_frequency)
atrv.append(camera)
camera.add_interface('ros',topic='/camera')"""

#laser 10Hz, 180 degrees wide with a 180 points
scan = Sick()
scan.translate(x=0.275, z=0.252)
scan.properties(Visible_arc = True,laser_range = 30.0,resolution = 1,scan_window = 180.0)
scan.frequency(5)
scan.create_laser_arc()
scan.add_interface('ros', topic='/scan',frame_id="laser", child_frame_id="base_link")
atrv.append(scan)

"""
INPUT: through keyboard
"""
# Allows to control the robot with the keyboard
keyboard = Keyboard()
atrv.append(keyboard)

"""
ATUADORES: through motion
"""
#motion controller
motion = MotionXYW()
atrv.append(motion)
motion.add_interface('ros', topic='/cmd_vel')

# Set the environment
env = Environment('/home/eduardo/TG_OFFICIAL/Morse/estacionamento')
env.set_camera_location([-25, -7, 2])
env.set_camera_rotation([1.0470, 0, 0.7854])
atrv.add_default_interface('ros')
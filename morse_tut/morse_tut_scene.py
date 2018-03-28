from morse.builder import *
 
atrv = ATRV() #the robot
atrv.translate(x=2.5, y=3.2, z=0.0) #starting location
 
# An odometry sensor to get odometry information
odometry = Odometry()
atrv.append(odometry)
odometry.add_interface('ros', topic="/odom",frame_id="odom", child_frame_id="base_link")
 
# Allows to control the robot with the keyboard
keyboard = Keyboard()
atrv.append(keyboard)
 
#camera 10Hz, 320x240 image
cam_frequency = 10
camera = VideoCamera()
camera.translate(x = 0.7, z= 0.5)
camera.rotate(y = -0.0)
camera.properties(cam_width=320,cam_height=240,cam_focal=6.,cam_near=0.1,cam_far=500)
camera.frequency(cam_frequency)
atrv.append(camera)
camera.add_interface('ros',topic='/camera')
 
#laser 10Hz, 180 degrees wide with a 180 points
scan = Hokuyo()
scan.translate(x=0.275, z=0.252)
atrv.append(scan)
scan.properties(Visible_arc = True,laser_range = 30.0,resolution = 1,scan_window = 180.0)
scan.frequency(10)
scan.create_laser_arc()
scan.add_interface('ros', topic='/scan',frame_id="laser", child_frame_id="base_link")
 
#motion controller
motion = MotionXYW()
atrv.append(motion)
motion.add_interface('ros', topic='/cmd_vel')
 
# Set the environment
env = Environment('indoors-1/indoor-1')

#commentS
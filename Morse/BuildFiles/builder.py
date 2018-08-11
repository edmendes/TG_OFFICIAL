from morse.builder import *
 
atrv = ATRV() #the robot
atrv.translate(x=-31, z=-4.9) #starting location
atrv.rotate(z=3.14/2)

#motion controller
motion = MotionXYW()
atrv.append(motion) #Add a child to the current object
motion.add_interface('ros', topic='/cmd_vel') #Add a service and stream interface to the component
motion.add_stream('ros') #Add a data stream interface to the component

pose = Pose()
pose.translate(z=0.83)
atrv.append(pose)
pose.add_interface('ros', topic='/pose')
'''
pose.add_stream('ros')'''
 
# An odometry sensor to get odometry information
odometry = Odometry()
atrv.append(odometry)
odometry.add_interface('ros', topic="/odom",frame_id="odom", child_frame_id="base_link")
odometry.add_stream('ros')
 
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
cam_d = DepthCamera()
cam_d.translate(x=0.7,z=0.94)
atrv.append(cam_d)
cam_d.properties(cam_width=320,cam_height=240,cam_focal=6.,cam_near=0.1,cam_far=500)
cam_d.add_interface('ros', topic='/scan',frame_id="laser", child_frame_id="base_link")
cam_d.add_stream('ros')
 
# Set the environment
env = Environment('/home/eduardo/TG_OFFICIAL/Morse/estacionamento')
env.set_camera_location([-25, -7, 2])
env.set_camera_rotation([1.0470, 0, 0.7854])
#env = Environment('indoors-1/indoor-1')
atrv.add_default_interface('ros')




#
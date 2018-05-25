from morse.builder import *
 
atrv = ATRV() #the robot
atrv.translate(x=-31, y=1, z=-5) #starting location
atrv.rotate(z=3.14/2)

#adding a dumb robot 
atrv1 = ATRV() #the robot
atrv1.translate(x=-25, y=5, z=-4.9) #starting location
atrv1.rotate(z=3.14/2)

#adding a passive object
table = PassiveObject('props/objects','SmallTable')
table.setgraspable()
table.translate(x=-35, y=35, z=-4.9)
table.properties(Type = "table", Object = True, Graspable = True, Label = "TABLE")

table = PassiveObject('props/objects','SmallTable')
table.setgraspable()    
table.translate(x=35, y=35, z=-4.9)
table.properties(Type = "table", Object = True, Graspable = True, Label = "TABLE")

table3 = PassiveObject('props/objects','SmallTable')
table3.setgraspable()
table3.translate(x=35, y=-35, z=-4.9)
table3.properties(Type = "table", Object = True, Graspable = True, Label = "TABLE")

table4 = PassiveObject('props/objects','SmallTable')
table4.setgraspable()
table4.translate(x=-35, y=-35, z=-4.9)
table4.properties(Type = "table", Object = True, Graspable = True, Label = "TABLE")

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

""" The type of detected objects. This type is looked for as a game property of scene objects or as their ‘Type’ property. You must then add fix this property to the objects you want to be detected by the semantic camera. """
camera = SemanticCamera()
atrv.append(camera)
camera.properties(tag = "table",cam_width=320,cam_height=240,cam_focal=6.,cam_near=0.1,cam_far=100000000, scan_window = 180.0)
camera.translate(x=0.3, z=0.762)
camera.add_interface('ros',topic='/camera',frame_id="odom", child_frame_id="base_link")

#Infrared 
infraredEs1 = Sick()
infraredEs1.properties(Visible_arc = True,laser_range = 5,resolution = 1,scan_window = 50)
infraredEs1.translate(0, 0.35, 0) 
infraredEs1.rotate(0, 0, 1.57)
infraredEs1.create_laser_arc()
infraredEs1.frequency(5)
infraredEs1.add_interface('ros', topic='/scan1',frame_id="laser", child_frame_id="base_link")
atrv.append(infraredEs1)

#laser 10Hz, 180 degrees wide with a 180 points
scan = Sick()
scan.translate(x=0.3, z=0.452)
scan.properties(Visible_arc = True,laser_range = 20.0,resolution = 1,scan_window = 60)
scan.frequency(1)
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
env.set_camera_location([-26.5, 27, 2])
env.set_camera_rotation([1.0470, 0, 3*0.7854])
atrv.add_default_interface('ros')
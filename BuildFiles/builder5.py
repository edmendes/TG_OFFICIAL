from morse.builder import *
 
atrv = ATRV() #the robot
atrv.translate(x=-31, y=1, z=-5) #starting location
atrv.rotate(z=3.14/2)

#adding a dumb robot 
atrv1 = ATRV() #the robot
atrv1.translate(x=-25, y=5, z=-4.9) #starting location
atrv1.rotate(z=3.14/2)

#adding a passive object


box0_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_0.translate(x=-175.99, y=34.37, z=-4.29)
box0_0.properties(Object = True, Label = "BOX")

box0_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_1.translate(x=-163.73, y=34.61, z=-4.29)
box0_1.properties(Object = True, Label = "BOX")

box0_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_2.translate(x=-117.91, y=34.59, z=-4.29)
box0_2.properties(Object = True, Label = "BOX")

box0_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_3.translate(x=-105.89, y=34.59, z=-4.29)
box0_3.properties(Object = True, Label = "BOX")

box0_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_4.translate(x=-35.24, y=34.59, z=-4.29)
box0_4.properties(Object = True, Label = "BOX")

box0_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_5.translate(x=-23.22, y=34.59, z=-4.29)
box0_5.properties(Object = True, Label = "BOX")

box0_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_6.translate(x=22.62, y=34.59, z=-4.29)
box0_6.properties(Object = True, Label = "BOX")

box0_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_7.translate(x=34.64, y=34.59, z=-4.29)
box0_7.properties(Object = True, Label = "BOX")

box0_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_8.translate(x=105.28, y=34.59, z=-4.29)
box0_8.properties(Object = True, Label = "BOX")

box0_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_9.translate(x=117.29, y=34.59, z=-4.29)
box0_9.properties(Object = True, Label = "BOX")

box0_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_10.translate(x=163.14, y=34.59, z=-4.29)
box0_10.properties(Object = True, Label = "BOX")

box0_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box0_11.translate(x=175.17, y=34.59, z=-4.29)
box0_11.properties(Object = True, Label = "BOX")

box1_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_0.translate(x=-175.59, y=22.32, z=-4.29)
box1_0.properties(Object = True, Label = "BOX")

box1_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_1.translate(x=-163.93, y=22.32, z=-4.29)
box1_1.properties(Object = True, Label = "BOX")

box1_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_2.translate(x=-117.72, y=22.32, z=-4.29)
box1_2.properties(Object = True, Label = "BOX")

box1_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_3.translate(x=-106.07, y=22.32, z=-4.29)
box1_3.properties(Object = True, Label = "BOX")

box1_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_4.translate(x=-35.06, y=22.32, z=-4.29)
box1_4.properties(Object = True, Label = "BOX")

box1_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_5.translate(x=-23.4, y=22.32, z=-4.29)
box1_5.properties(Object = True, Label = "BOX")

box1_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_6.translate(x=22.8, y=22.32, z=-4.29)
box1_6.properties(Object = True, Label = "BOX")

box1_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_7.translate(x=34.45, y=22.32, z=-4.29)
box1_7.properties(Object = True, Label = "BOX")

box1_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_8.translate(x=105.46, y=22.32, z=-4.29)
box1_8.properties(Object = True, Label = "BOX")

box1_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_9.translate(x=117.12, y=22.32, z=-4.29)
box1_9.properties(Object = True, Label = "BOX")

box1_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_10.translate(x=163.35, y=22.32, z=-4.29)
box1_10.properties(Object = True, Label = "BOX")

box1_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box1_11.translate(x=174.98, y=22.32, z=-4.29)
box1_11.properties(Object = True, Label = "BOX")

box2_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_0.translate(x=-175.76, y=-23.27, z=-4.29)
box2_0.properties(Object = True, Label = "BOX")

box2_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_1.translate(x=-163.75, y=-23.27, z=-4.29)
box2_1.properties(Object = True, Label = "BOX")

box2_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_2.translate(x=-117.9, y=-23.27, z=-4.29)
box2_2.properties(Object = True, Label = "BOX")

box2_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_3.translate(x=-105.88, y=-23.27, z=-4.29)
box2_3.properties(Object = True, Label = "BOX")

box2_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_4.translate(x=-35.27, y=-23.27, z=-4.29)
box2_4.properties(Object = True, Label = "BOX")

box2_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_5.translate(x=-23.43, y=-23.24, z=-4.29)
box2_5.properties(Object = True, Label = "BOX")

box2_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_6.translate(x=22.59, y=-23.24, z=-4.29)
box2_6.properties(Object = True, Label = "BOX")

box2_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_7.translate(x=34.66, y=-23.25, z=-4.29)
box2_7.properties(Object = True, Label = "BOX")

box2_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_8.translate(x=105.27, y=-23.27, z=-4.29)
box2_8.properties(Object = True, Label = "BOX")

box2_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_9.translate(x=117.32, y=-23.24, z=-4.29)
box2_9.properties(Object = True, Label = "BOX")

box2_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_10.translate(x=163.14, y=-23.27, z=-4.29)
box2_10.properties(Object = True, Label = "BOX")

box2_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box2_11.translate(x=175.19, y=-23.27, z=-4.29)
box2_11.properties(Object = True, Label = "BOX")

box3_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_0.translate(x=-175.59, y=-35.54, z=-4.29)
box3_0.properties(Object = True, Label = "BOX")

box3_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_1.translate(x=-163.96, y=-35.52, z=-4.29)
box3_1.properties(Object = True, Label = "BOX")

box3_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_2.translate(x=-117.69, y=-35.52, z=-4.29)
box3_2.properties(Object = True, Label = "BOX")

box3_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_3.translate(x=-105.86, y=-35.32, z=-4.29)
box3_3.properties(Object = True, Label = "BOX")

box3_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_4.translate(x=-35.06, y=-35.54, z=-4.29)
box3_4.properties(Object = True, Label = "BOX")

box3_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_5.translate(x=-23.4, y=-35.54, z=-4.29)
box3_5.properties(Object = True, Label = "BOX")

box3_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_6.translate(x=22.83, y=-35.52, z=-4.29)
box3_6.properties(Object = True, Label = "BOX")

box3_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_7.translate(x=34.43, y=-35.52, z=-4.29)
box3_7.properties(Object = True, Label = "BOX")

box3_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_8.translate(x=105.49, y=-35.52, z=-4.29)
box3_8.properties(Object = True, Label = "BOX")

box3_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_9.translate(x=117.12, y=-35.54, z=-4.29)
box3_9.properties(Object = True, Label = "BOX")

box3_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_10.translate(x=163.33, y=-35.54, z=-4.29)
box3_10.properties(Object = True, Label = "BOX")

box3_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box3_11.translate(x=174.96, y=-35.52, z=-4.29)
box3_11.properties(Object = True, Label = "BOX")

box4_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_0.translate(x=-175.77, y=-105.93, z=-4.29)
box4_0.properties(Object = True, Label = "BOX")

box4_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_1.translate(x=-163.93, y=-105.93, z=-4.29)
box4_1.properties(Object = True, Label = "BOX")

box4_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_2.translate(x=-117.9, y=-105.93, z=-4.29)
box4_2.properties(Object = True, Label = "BOX")

box4_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_3.translate(x=-105.88, y=-105.93, z=-4.29)
box4_3.properties(Object = True, Label = "BOX")

box4_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_4.translate(x=-35.24, y=-105.93, z=-4.29)
box4_4.properties(Object = True, Label = "BOX")

box4_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_5.translate(x=-23.23, y=-105.93, z=-4.29)
box4_5.properties(Object = True, Label = "BOX")

box4_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_6.translate(x=22.6, y=-105.93, z=-4.29)
box4_6.properties(Object = True, Label = "BOX")

box4_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_7.translate(x=34.67, y=-105.9, z=-4.29)
box4_7.properties(Object = True, Label = "BOX")

box4_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_8.translate(x=105.93, y=-105.9, z=-4.29)
box4_8.properties(Object = True, Label = "BOX")

box4_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_9.translate(x=117.3, y=-105.9, z=-4.29)
box4_9.properties(Object = True, Label = "BOX")

box4_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_10.translate(x=163.14, y=-105.93, z=-4.29)
box4_10.properties(Object = True, Label = "BOX")

box4_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box4_11.translate(x=175.16, y=-105.93, z=-4.29)
box4_11.properties(Object = True, Label = "BOX")

box5_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_0.translate(x=-175.59, y=-118.2, z=-4.29)
box5_0.properties(Object = True, Label = "BOX")

box5_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_1.translate(x=-163.93, y=-118.2, z=-4.29)
box5_1.properties(Object = True, Label = "BOX")

box5_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_2.translate(x=-117.7, y=-118.19, z=-4.29)
box5_2.properties(Object = True, Label = "BOX")

box5_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_3.translate(x=-106.06, y=-118.2, z=-4.29)
box5_3.properties(Object = True, Label = "BOX")

box5_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_4.translate(x=-35.06, y=-118.2, z=-4.29)
box5_4.properties(Object = True, Label = "BOX")

box5_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_5.translate(x=-23.4, y=-118.2, z=-4.29)
box5_5.properties(Object = True, Label = "BOX")

box5_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_6.translate(x=22.83, y=-118.2, z=-4.29)
box5_6.properties(Object = True, Label = "BOX")

box5_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_7.translate(x=34.46, y=-118.2, z=-4.29)
box5_7.properties(Object = True, Label = "BOX")

box5_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_8.translate(x=105.46, y=-118.2, z=-4.29)
box5_8.properties(Object = True, Label = "BOX")

box5_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_9.translate(x=117.12, y=-118.2, z=-4.29)
box5_9.properties(Object = True, Label = "BOX")

box5_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_10.translate(x=163.33, y=-118.2, z=-4.29)
box5_10.properties(Object = True, Label = "BOX")

box5_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box5_11.translate(x=174.98, y=-118.2, z=-4.29)
box5_11.properties(Object = True, Label = "BOX")

box6_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_0.translate(x=-175.76, y=-163.8, z=-4.29)
box6_0.properties(Object = True, Label = "BOX")

box6_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_1.translate(x=-163.75, y=-163.8, z=-4.29)
box6_1.properties(Object = True, Label = "BOX")

box6_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_2.translate(x=-117.94, y=-163.77, z=-4.29)
box6_2.properties(Object = True, Label = "BOX")

box6_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_3.translate(x=-105.88, y=-163.79, z=-4.29)
box6_3.properties(Object = True, Label = "BOX")

box6_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_4.translate(x=-35.24, y=-163.8, z=-4.29)
box6_4.properties(Object = True, Label = "BOX")

box6_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_5.translate(x=-23.22, y=-163.8, z=-4.29)
box6_5.properties(Object = True, Label = "BOX")

box6_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_6.translate(x=22.61, y=-163.8, z=-4.29)
box6_6.properties(Object = True, Label = "BOX")

box6_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_7.translate(x=34.64, y=-163.8, z=-4.29)
box6_7.properties(Object = True, Label = "BOX")

box6_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_8.translate(x=105.28, y=-163.8, z=-4.29)
box6_8.properties(Object = True, Label = "BOX")

box6_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_9.translate(x=117.29, y=-163.8, z=-4.29)
box6_9.properties(Object = True, Label = "BOX")

box6_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_10.translate(x=163.15, y=-163.8, z=-4.29)
box6_10.properties(Object = True, Label = "BOX")

box6_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box6_11.translate(x=175.16, y=-163.8, z=-4.29)
box6_11.properties(Object = True, Label = "BOX")

box7_0 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_0.translate(x=-175.59, y=-176.07, z=-4.29)
box7_0.properties(Object = True, Label = "BOX")

box7_1 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_1.translate(x=-163.92, y=-176.07, z=-4.29)
box7_1.properties(Object = True, Label = "BOX")

box7_2 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_2.translate(x=-117.73, y=-176.07, z=-4.29)
box7_2.properties(Object = True, Label = "BOX")

box7_3 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_3.translate(x=-106.07, y=-176.07, z=-4.29)
box7_3.properties(Object = True, Label = "BOX")

box7_4 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_4.translate(x=-35.06, y=-176.07, z=-4.29)
box7_4.properties(Object = True, Label = "BOX")

box7_5 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_5.translate(x=-23.44, y=-176.07, z=-4.29)
box7_5.properties(Object = True, Label = "BOX")

box7_6 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_6.translate(x=22.8, y=-176.07, z=-4.29)
box7_6.properties(Object = True, Label = "BOX")

box7_7 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_7.translate(x=34.27, y=-176.07, z=-4.29)
box7_7.properties(Object = True, Label = "BOX")

box7_8 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_8.translate(x=105.46, y=-176.07, z=-4.29)
box7_8.properties(Object = True, Label = "BOX")

box7_9 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_9.translate(x=117.12, y=-176.07, z=-4.29)
box7_9.properties(Object = True, Label = "BOX")

box7_10 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_10.translate(x=163.33, y=-176.07, z=-4.29)
box7_10.properties(Object = True, Label = "BOX")

box7_11 = PassiveObject('/home/eduardo/morse-1.3/data/props/box','RedBox')
box7_11.translate(x=174.98, y=-176.07, z=-4.29)
box7_11.properties(Object = True, Label = "BOX")
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
env = Environment('/home/eduardo/TG_OFFICIAL/Morse/autoroad')
env.set_camera_location([-26.5, 27, 2])
env.set_camera_rotation([1.0470, 0, 3*0.7854])
atrv.add_default_interface('ros')
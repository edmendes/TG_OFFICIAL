#16  de julho - 17h00
#teste_MORSE_1 - Edu e Nathalia 

from morse.builder import *
#Robo -- MORSE knows three main components: the robots, the sensors and the actuators (the robots are mostly supports for sensors or actuators).
# ATRV 4 = wheeled outdoor robot.

atrv = ATRV()
atrv.translate(x=-31, z=-4.9)
atrv.rotate (z = 3.14/2)

#Atuador -- MOtionVW (v,omega) - This one controls the robot by changing the linear and angular velocity of the movement.

motion = MotionVW()
motion.translate(z=0.3)
atrv.append(motion)

#Sensors -- Pose sensor, which provides us with the location and rotation of the robot.

pose = Pose()
pose.translate(z=0.82)
atrv.append(pose)
cam  = VideoCamera() #Camera - adding a video camera and changing its properties
cam.properties(cam_width = 128, cam_height = 128)
atrv.append(cam)

#Middlewares -- basic socket to access the data-streams and services provided by the components. 

pose.add_stream('ros')
motion.add_stream('ros')
#pose.add_service('socket')
#motion.add_service('socket')

#Environment -- The Environment method is the name of a Blender .blend file you provide (with its full path) or a pre-defined one.

#The Environment object also provides additional options to place and aim the default camera, by using the methods set_camera_rotation and set_camera_location.

#env = Environment('indoors-1/indoor-1')

env = Environment('/home/eduardo/Documents/TG_OFFICIAL/Morse/estacionamento')
env.set_camera_location([-25, -7, 2])
env.set_camera_rotation([1.0470, 0, 0.7854])

#connection to sockets: communication to simulation @ Blender
# on terminal: $ telnet localhost 4000

#The motion controller we have added to the robot export one service, set_speed: to make the robot move in a circle, with linear speed 2 m/s and angular speed -1 rad/s

#id1 atrv.motion set_speed [2, -1]

#id1 = identifier
#the internal name of the component is (here, atrv.motion) is displayed in the MORSE log at the end of the simulation initialisation.

#id2 atrv.pose get_local_data

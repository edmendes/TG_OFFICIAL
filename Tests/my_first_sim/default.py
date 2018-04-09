#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <my_first_sim> environment

Feel free to edit this template as you like!
"""

from morse.builder import *

robot = ATRV()

# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
robot.translate(1.0, 0.0, 0.0)
robot.rotate(0.0, 0.0, 3.5)

motion = MotionVW()
robot.append(motion)

#scanner sensor
sick = Sick()
sick.translate(0.5, 0.0, 0.5)
sick.rotate(0.0, 0.0, 0)
sick.add_interface('socket')
robot.append(sick)

# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# 'morse add sensor <name> my_first_sim' can help you with the creation of a custom
# sensor.
pose = Pose()
robot.append(pose)

#interface
robot.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
env = Environment('indoors-1/boxes', fastmode = False)
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])


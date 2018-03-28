#! /usr/bin/env morseexec
#
# http://www.openrobots.org/morse/doc/latest/user/builder.html
# http://www.openrobots.org/morse/doc/latest/user/builder_overview.html  # GOOD
# http://www.openrobots.org/morse/doc/latest/user/code/morse.builder.html
#
# Add service (Remote Procedure Call) to a component ...
# http://www.openrobots.org/morse/doc/latest/dev/services.html

from morse.builder import *

# All components should be able to be modified ...
#   location = (x,y,z) : absolute
#   rotation_euler = (x,y,z) : absolute
#   scale = (x,y,z)
#   translate(x,y,z) : relative
#   rotate(x,y,z) : relative
#   append(component)
#   frequency(hz)
#   level(level)
#   properties()
#   alter(modifier)

# Add manditory robot(s)

robot_army_count = 1

for i in range(robot_army_count):
# robot = ATRV('robot')
# robot = Morsy('robot')
# robot = Quadrotor('robot')
  robot = RMax('robot')
# robot.properties(NoGravity=True, GroundRobot=True)
# robot.name = "nexus-1"
  robot.translate(15.0, 20.0, 10.0)  # Can translate() any component
# robot.rotate(0.0, 0.0, 3.5)     # Can rotate() any component

# Add camera
# Can change properties() of any component or add new properties()

camera = VideoCamera()
camera.properties(cam_width=256, cam_height=256)
camera.translate(x=0.0, y=0.0, z=0.0)
camera.rotate(0.0, -0.3491, 0.0)
robot.append(camera)
# camera.properties(cam_far=800)
camera.add_stream('socket')  # for external Python script

# ptu = PTU()
# robot.append(ptu)

# Append an odometry sensor
odometry = Odometry()
odometry.translate(x=-0.1, z=0.83)
robot.append(odometry)

# Append a proximity sensor
proximity = Proximity()
proximity.translate(x=-0.2, z=0.83)
robot.append(proximity)

# Append a sick laser
sick = Sick()
sick.translate(x=0.18,z=0.94)
robot.append(sick)
sick.properties(resolution = 1)
sick.properties(laser_range = 5.0)

# Add keyboard controller
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Add actuator

motion = MotionVW()
robot.append(motion)

# See compatibility matrix ...
#  http://www.openrobots.org/morse/doc/latest/user/integration.html
# motion.add_stream('ros')
# motion.add_stream('yarp')

# motion.add_interface('socket') ... is the same as ...
#   motion.add_stream('socket')
#   motion.add_service('socket')

# Add sensor

pose = Pose()
pose.translate(z = 0.75)
robot.append(pose)

# Add component modifier ...
# http://www.openrobots.org/morse/doc/latest/user/modifier_introduction.html
# pose.alter('Noise', pos_std=0.3)

# Configure the robot on the 'socket' interface
# $ telnet localhost 4000
#   Connected to localhost.
#   > req1 robot.motion set_speed [1.0, 0.002]
#   req1 SUCCESS
#   > req2 robot.motion set_speed [0.0, 0.000]
#   req2 SUCCESS

robot.add_default_interface('socket')

# Environment() must be the last line of the file
# http://www.openrobots.org/morse/doc/latest/user/code/morse.builder.html#morse.builder.environment.Environment
#
# fastmode=False  # Full Blender rendering
# fastmode=True   # Wireframe rendering, no vision based sensors
#
# See /usr/local/share/morse/data/environments/indoors-1/indoor-1.blend
# export MORSE_RESOURCE_PATH="/usr/local/share/morse:/some/where/else"

# env = Environment('indoors-1/indoor-1', fastmode=False)
# env = Environment('sandbox', fastmode=False)

env = Environment('land-1/trees')
env.set_camera_location([6.0, 25.0, 10.0])
env.set_camera_rotation([1.5708, 0.0, -1.5708])  # 90 degrees= 1.5708 radians

env.select_display_camera(camera)
env.set_camera_clip(clip_end=1000)
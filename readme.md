
README

This project was developed by Eduardo Mendes and Nathalia Paula to accomplish the final requirements for the course of Bachelor's in Instrumentation, Automation and Robotic Engineering at University Federal of ABC, located in Santo André, Brazil.

The main objective is to develop an autonomous robot able to move in a predetermined environment, moving from point A to point B. The robot must learn the best routes and after some iterations, it should find an optimal solution. Therefore, it was used the Q-Learning theory.

Watch the simulation results video here: https://youtu.be/q8ctXwmutXo

Contributors email:

eduardo DOT mendes AT aluno DOT ufabc DOT edu DOT br 

nathalia DOT paula AT aluno DOT ufabc DOT edu DOT br 

1) To run this project, it is needed to install Ubuntu 14.04, ROS Indigo and the last Blender version.

2) After all installation process, you must follow three simple steps to run the file:
Step 0 - Clone the folder "working_version" into your computer.

Step 1 - Open the terminal window and type "roscore", in order to be run ROS.

Step 2 - In another terminal, you must run the builder file. Thus, type:

```
morse run builder.py
```

Step 3 - Open a new terminal select the folder type:

```
python Node.py
```

obs: remember to change the file .blend location in builder.pya
=====


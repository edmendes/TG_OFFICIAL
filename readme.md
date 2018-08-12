
**Q-Learning autonomous mobile robot - ROS + MORSE Simulation**

This project was developed by Eduardo Mendes and Nathalia Paula to accomplish the final requirements for the course of Bachelor's in Instrumentation, Automation and Robotic Engineering at University Federal of ABC, located in Santo André, Brazil.

The main objective is to develop an autonomous mobile robot able to move in a unknown 3D environment, moving from a ramdom point and find a fixed target destination. The robot must learn from this policy using Q-Learning algorithm:

> Achieve a fixed (x<sub>t</sub>, y<sub>t</sub>, z<sub>t</sub>) target in a unknown environment from 10 random (x<sub>p</sub>, y<sub>p</sub>, z<sub>p</sub>) start points, whose number of steps is minimal.


Watch the simulation results here: https://youtu.be/q8ctXwmutXo

<center><a href="http://www.youtube.com/watch?feature=player_embedded&v=q8ctXwmutXo
" target="_blank"><img src="http://img.youtube.com/vi/q8ctXwmutXo/0.jpg" 
alt="Q-learning agent simulation video" width="720" height="540" border="5" /></a></center>

Contributors email:

eduardo DOT mendes AT aluno DOT ufabc DOT edu DOT br 

nathalia DOT paula AT aluno DOT ufabc DOT edu DOT br 

i) To run this project, it is needed to install Ubuntu 14.04, ROS Indigo and the last Blender version.

ii) After all installation process, you must follow three simple steps to run the file:

Step 0: Clone the folder "working_version" into your computer.

Step 1: Open the terminal window and type "roscore", in order to be run ROS.

Step 2: In another terminal, you must run the builder file. Thus, type:

```
morse run builder_base.py
```

Step 3 - Open a new terminal select the folder type:

```
python Node.py
```

> **Obs. 1: the code from "working_version" is the lastest version, which agent was full trained. To reset the learning training, remove "tableq.csv" and "q_evolution.json" files**

> **Obs. 2: remember to change the file .blend location in builder.pya**




## Getting Started in a right way to run ROS file with Morse ;)

Step 0 - On Terminal, type 
```
$ gedit ~/.bashrc
```
, go to the bottom of file and add this line:
```
$ source ~/catkin_ws/devel/setup.bash
```

Step 1 - create a new catkin package (named as AutonomousCarQ, it will be our Project Root Folder ROS-like structured): http://wiki.ros.org/ROS/Tutorials/CreatingPackage

Step 2 - Access that package through roscd

Step 3 - Code Morse environment and robot parameters (morse / builder.py) and save it in a morse folder (create it) within AutonoumousCarQ package folder

Step 4 - Code ROS node (movements etc.) and do not forget at the right first line
```
#!/usr/bin/env python
```

Step 5 - In order to run more than one node only once instead of run each node in a terminal windown, you can create a ROS .launch file (car_nodes.launch) by following this tutorial: http://lsi.vc.ehu.es/pablogn/investig/ROS/A%20Gentle%20Introduction%20to%20ROS.pdf

Step 6 - to run a ROS node (rospy node file), you need to turn it into a executable node by typing 

```
$ #chmod +x PATH/your_node_file.py
```
Step 7 - Open a terminal window to run:
```
$ roscore
```
Step 8: Open another terminal window and run morse environment:

go to your morse package folder by typing:
```
$ roscd <package>/morse
```
or, in my case:
```
$ roscd AutonomousCarQ/morse
```
...  it must work! 

Inside morse folder, run morse as
```
$ morse run builder.py
```

Step 9 - Finnaly, in another terminal window open, run ROSPY: 
```
$ rospy <package> node.py
```
or, in my case:
```
$ rospy AutonomousCarQ car_node.py
```
Optional step: to run roslaunch instead of rospy (for each node), after created .launch file (car_nodes.launch), type:
```
$ roslaunch AutonomousCarQ car_nodes.launch
```



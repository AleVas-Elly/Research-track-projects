# ROS SLAM Exercise
## Third Assignment of the course Research_Track_1, Robotics Engineering, UNIGE.

-------------------

This project makes use of a set of software libraries [__ROS__](http://wiki.ros.org) (__Robot-Operating-Systems__) to build a robot application that makes a mobile robot run in a Labirint according to a few different modalities. 
The software (SW) indeed:

- uses the coordinates entered by the user to make the robot reach that pose.
- makes it possible to drive robots with keyboards
- implements a function that allows obstacle avoidance

The code is developed using the python programming language, making use of some useful libraries. (To be found in the initial part of the scripts)
Everything was developed on Ubuntu Focal Fossa (20.04) using ROS noetic distro.

Installing and running  
---------------------

__First things first!__

In order to install and run this project u must have some packages already installed, run the following commands to be sure everything is correctly set:

```bash
        sudo apt-get update
        sudo apt-get install konsole
        sudo apt-get install ros-<ros_distro>-gmapping
        sudo apt-get isntall ros-<ros_distro>-navigation
        sudo apt-get install python-actionlib
```
With the second command you are gonna install [__Konsole__](https://konsole.kde.org) which is gonna come in handy later.
With the last three commands u are respectively installing the [__gmapping package__](http://wiki.ros.org/gmapping),the [__navigation package__](http://wiki.ros.org/navigation) and the [__actionlib package__](http://wiki.ros.org/actionlib). They are all necessary for the SW to run properly. 
(More informations are retrievable following the links above)

__Running__

At this point u should have all the prerequisites for the SW to work properly. In order to get the developed SW just fork (or download) this repository in your workspace.
Now just:

- build ur workspace running:

```bash
    $catkin_make
```
To compile the new packages installed into the workspace, remember to run catkin_make while being in the workspace root directory!

POTREI FARE UN UNICO LAUNCH FILE CHE MI PERMETTA DI AVERE UN INTERFACCIA CHE MI POSSA FAR SCEGLIERE LA MODALITA'

- launch this two launch files:
```bash
        $roslaunch final_assignment simulation_gmapping.launch
        $roslaunch final_assignment move_base.launch
        ROSLAUNCH FINAL ASSIGNMEN UI.LAUNCH
```

Practically with the first launch file you start [__Gazebo__](https://gazebosim.org/home) and [__rviz__](http://wiki.ros.org/rviz) simulators through which u are gonna be able to see (or more generally interact with) the robot.

ROSCLEAN PURGE 

- To make the robot reach whatever location inside the maze the user wants run:

```bash
    $rosrun final_assignment to_user_pose.py

```

After running this command u will see the terminal window asking for the x and the y coordinates. The robot has a 30 seconds timeout to find the target, if the asked position is reached task ends, otherwise the task fails. In both cases the user is gonna be asked to enter new coordinates to reach.

- To make the user use the keyboard to drive the robot _without_ object avoidance run:

```bash
    $rosrun final_assignment key_avoid_OFF.py
```

- To "activate" obstacle avoidance just run:

```bash
    $roslaunch final_assignment obs_avoidance.launch
```
with __`obs_avoidance.launch`__ : 

```xml
<?xml version="1.0"?>
<launch>

    <node pkg="final_assignment" type="key_avoid_OFF.py" name="key_avoid_OFF" output="screen" launch-prefix="konsole -e" />
    <node pkg="final_assignment" type="wall_follow_service.py" name="wall_follow_service" output="screen" />
    <node pkg="final_assignment" type="obstacle_avoidance.py" name="obstacle_avoidance" output="screen" />
</launch>
```
Where, the first node allow the user to drive the robot with the keyboard, the second doesn't allow it to make it go against obstacles and the third is useful beacuse in case a wall is found to be near, it makes the robot follow it and not touch it even if the user would force it to do it.

__rqt__

In order to retrive more infos about the nodes and the topics, and about the overall architecture in general rqt could be a great tool!
In order to install it run:

```bash
  $ sudo apt-get install ros-noetic-rqt
```
and to launch it:

```bash
  $ rqt_graph
```

A few images to make at once the user acquainted with the project:

_The robot:_

![IMAGE 2022-04-24 16:15:19](https://user-images.githubusercontent.com/91626281/164980772-11fce6ac-435b-4227-a5d9-70088fc8cb99.jpg)

_The Maze:_

![IMAGE 2022-04-24 16:15:38](https://user-images.githubusercontent.com/91626281/164980784-7e4459c3-2268-42ba-9991-f5ac887218f8.jpg)

_What is seen by the robot (rviz screenshot) at the beginning of the simulation:_

![IMAGE 2022-04-24 16:16:28](https://user-images.githubusercontent.com/91626281/164980813-2b4952f2-ac2a-4dfb-87dc-cab033ebec7c.jpg)



METTI APPOSTO grafici





Dynamic graph of what’s going on:

![photo_2022-01-26_19-06-21](https://user-images.githubusercontent.com/80394968/151221363-f6d84de5-d43d-46db-ab85-bd5434a9b2ae.jpg)

Flowchart(General idea behind the program)
----------------------
Structure of the first part
![Immagine 2022-01-26 202719](https://user-images.githubusercontent.com/80394968/151232902-d5e477ba-b2c5-4b06-aea0-e8fb43b75c78.jpg)

Structure of the second and third part
![Immagine 2022-01-26 202822](https://user-images.githubusercontent.com/80394968/151233142-af56c67a-9ed2-47b2-88bd-e73f8d451c0e.jpg)


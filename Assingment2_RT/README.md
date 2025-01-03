# ROS Monza Carcontroller 
## Second Assignment of the course Research_Track_1, Robotics Engineering UNIGE.

-----------------------

This project makes use of a set of software libraries [__ROS__](http://wiki.ros.org) (__Robot-Operating-Systems__) to build a robot application that makes a robot run autonomously in a circuit.

The robot is practically a cube with laser scanners and the circuit is the Monza F1 circuit:

This is the initial situation:

<img width="457" alt="map" src="https://user-images.githubusercontent.com/91626281/156046726-9142565b-52ff-4ca2-b3b4-ce0719b55b38.png">

The Package
-----------
The package contains the C++ sources needed for the interaction with the robot (analyzed more in depth later in this README). 

Rules of the "game"
------------------
for the Robot: 
* always lapping in the clockwise direction
* avoiding the walls
* being able to accelerate or decelerate according to the user's will
* resetting its position to the starting one if asked to do so

Installing and running  
---------------------

In order to run more than one node at the same time i decided to create a `.launch` file named `toRun.launch`.

__`toRun.launch`__ : 
```xml
<launch>	
	<node name="carcontroller_node" pkg="secondAssignment" type="carcontroller_node" output="screen" launch-prefix="xterm -e" required="true"/>
	<node name="UI_node" pkg="secondAssignment" type="UI_node" output= "screen" required="true"/>
	<node name="stageros" pkg="stage_ros" type="stageros" required ="true" args = "$(find secondAssignment)/world/my_world.world"/>
</launch>

```

__Commands to launch the project__:

At first make sure to have xterm installed, if not run: 
```bash
	sudo apt-get install xterm
```
(this is just to make the UI more functional, since it is gonna open a new terminal to display the instant velocity)

After cloning the repository in ur workspace and building it with the command

```bash
	catkin_make
```
just use the next command to make the simulation start

```bash
	roslaunch secondAssignment toRun.launch
```
where `secondAssignment` is the name of the ros package I created.

What did i do ?
---------------

I created two nodes: 
* One to control autonomously the movement of the robot.
* The second to create a really basic User Interface(UI) to increase or decrease in run-time the velocity, and also to reset the robot position to the starting one.

## Node Analysis

StageRos_Node
-------------
The stageros node simulates a world as defined in the `my_world.world` file in the world folfer. This file tells Stage everything about the environment which in our case is a representation of the Monza Formula 1 circuit.

Stageros Node subscribes to the topic `cmd_vel` from `geometry_msgs` package which provides a [`Twist`](https://docs.ros.org/en/api/geometry_msgs/html/msg/Twist.html) type message to express the velocity of a robot (linear and angular components).

The Stageros Node also publishes on the `base_scan` topic from `sensor_msgs` package which provides a [`LaserScan`](https://docs.ros.org/en/api/sensor_msgs/html/msg/LaserScan.html) type message. 

Eventually i also used a standard service called `reset_position` from the `std_srvs` package. 

UI_Node 
-------

This node manages the UI of the project. 
The user can control the speed of the robot by increasing and decreasing its acceleration. 
He can also reset the robot's position to its initial state.
The UI node receives input from a terminal window.

[__[a]__]   To Accelerate

[__[d]__]  To Decelerate

[__[r]__]   To Reset the position


As soon as an input arrives from outside, it is transmitted to the Controller_Node, which answers back sending the "robot's acceleration".
This is a client-server architecture and has been implemented by creating a custom service called Accelerate.srv.

Structure of the service:
``` xml
     char input
     ---
     float32 value
```
Where:
* __char__ input is the character typed by the user on the keyboard: __[a]__ , __[d]__ or __[r]__.

* __float32__ value is the "acceleration of the robot". 

Controller_Node 
---------------

This is the most important node of the package and it contains the logic for the robot's movement and for the handling of the inputs coming from the UI_Node. 

The Node is implemented in controller.cpp in the folder src.

The function implemented in this node are:

 * __Wall_detection(range_min, range_max , Laser_Array)__

This function is needed to compute the minimum distance betwen the robot and the walls.
It eanbles the sensor to detect an obstacle in a cone between the range_min and the range_max (not expressed in degrees but in the number of elements of an array of 721 elements). The array is read from the `base_scan` topic and it returns the distances between the robot and the circuit contour. The robot in this case in non holonomic, therefore the f.o.w. of the sensor is the 180 degrees in front of him.

   	`Arguments` :

   	* range_max (`int`) : the top end of the array Laser_Scan (721th value)

	* range_min (`int`) : the lower end of the array Laser_Scan (1st value)

   	* Laser_Scan (`float`) : the array of 721 elements representing the 180° field of view in front of the robot.

   	`Returns` :

   	* lowest_value (`float`) : the minimum value of the array (the minimum distance between the robot and the walls in the interval considered).

* __RotCallback__

This Callback function will be called whenever a message is posted on the `base_scan` topic.

Thanks to the function Wall_Detection(), the robot can detect the shortest distance to the walls on its right, left and front :

``` C++

	dist_front = Wall_Detection(310,410,Laser_Array); // shortest distance to wall on front

	dist_right = Wall_Detection(0,100,Laser_Array); // shortest distance to wall on the right 
	
	dist_left = Wall_Detection(620,720,Laser_Array); //  shortest distance to wall on teh left 

	// the 100 range is an empiric value


```

The Logic implemented to move the robot:

At first the robot checks for the presence of a wall in front of it at a distance of less than 1.5, if there isn't, it will move straight ahead, it publishes a linear velocity on the "cmd_vel" topic which is by default equal to 2 (again empiric value). 
If the wall is closer to the right, it will turn left and, if the wall is closer to the left, it will turn right.

* __Server__

The actual server to receive the client request from the UI_Node.

Here is where the user's keyboard input is received. A switch handles the different client requests. (__[a]__, __[d]__), __[r]__).

Acceleration and deceleration features are coded using a ,global variable that in the case of the former is incremented and in the case of the latter decremented.
The reset resets also the velocity of the robot. (bringing it back to 2)

Is created with this function also the server's response to the client's request;
The "response" is the float containing the degree of acceleration (the value of the global variable mentioned before), that is gonna get printed to screen.

Moreover if  by any chance the user inputs a wrong key a message of error will appear.

* __Reaccelerate__

Of course the faster the robot the more probabilities there is for it to crush into the walls, just like cars in real life actually! To overcome this issue i tried to make the robot reaccelerate just after a curve (exactly how a normal car would do). With the help of a boolean indeed the program knows if the robot has just approached a curve or if it is coming from a linear path. After it completes a curve the robot will gradually accelerate back to the UI imposed velocity.


Flowchart
----------------------
The flow chart of the project: 

![Untitled Diagram drawio](https://user-images.githubusercontent.com/91626281/156046687-189a83a2-2060-43ec-a166-a7f7cd6865ab.png)


Improvements ?
----------------------
* Maybe could be useful to implement a "Starting the curve" function, in order to make the robot path smoother and to make it goes faster.
For the pupose of speed, we could also maybe try to devide the f.o.w. of the robot in more slices (not only 3) in order to retrive more data, with the aim of a more precise control of the robot during curves.
More precisely i think that computing always the "freest" direction, so the direction where the wall is more distant from the robot, should be a good first step. Of course this approach must take into account that the robot has its own dimensions and it is not just a point. (robot could hit the wall with the lateral edges for example)

* Change the name secondAssignment in second_assignment since ROS has troubles with caps lock packages names.

* Using the default (Gnome) terminal of Ubuntu 20.04 in order to avoid the installation of xterm 
(I couldn't actually make it work with Gnome, it popped up an error when running the launch file, probably linked to a wrong syntax in the launch file itself)











 




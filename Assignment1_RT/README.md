# Python Robotics Simulator

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

## Installing and running

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).
Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

## Robot API

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.
The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.
To drop the token, call the `R.release` method.
Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.
Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

[sr-api]: https://studentrobotics.org/docs/programming/sr/

# The Assignment
The assignment consits in developing a program that makes the robot coninuously traveling along the circuit counter clockwise without crushing into walls. If the robot encounters a silver token on its path, it should grab it, put it behind it, and keep on going.
The idea i had to perform this task, is to make the robot always go forward until it encounters a a silver token or golden (or arena) one. In the former case the robot is gonna put the token behind itslef, in the latter he has to make a decision on which direction it should take in order to keep going counterclocwise. This decision is made through a simple mapping of the number of golden token near the robot at every encounter with a wall. Indeed it always decides turn towards the "freest" direction (without turning too much in order to prevent inversions in the route).

## The Pseudo code:
```python

*Assigning* values to: 
                      -threshold to control of orientation
                      -threshold to control of the linear distance
                      -threshold to enstabilish the range of view of the robot for silver tokens
                      -turning angle when a golden token is too near

*Initializing* a variable as an instance of the class Robot

*definition* of the function Drive() to make the robot go forward

*definition* of the function Turn() to make the robot turn

*definition* of the function find_silver_token() that makes the robot find the closest silver token in a certain circle of ray r and in a specific field of view (-45deg, +45deg)

*definition* of the function grab_and_turn() that makes the robot move the token behind itself

*definition* of widen_range() that widen the range in a particular case in which the robot doesn't exactly know where to turn

*definition* which_direction() that decides which direction to turn to when the robot is too near to a golden token
...
call to widen_range() if it can't decide which direction to take
...

*definition* of avoid_walls() to make the robot avvoid walls 
...
 call to which_direction()
...

main()
   while(True)
      if the robot can't see any wall
         go forward
         avoid_walls()
      elif the S. token is near and in front
         it puts it behind it
      elif the S.token is well aligned with the robot
         go forward
      elif if the S.token is on the right 
         turn left
      elif the S.token is on the left
         turn right
```

### You can run the Assignment with:

```bash
$ python run.py Assignment1.py
```
## Conclusions and afterthoughts

The program has been tested for 15 mins multiple times and the robot has never touched a wall or inverted its route.
Possible improvements can be done to the pace of the robot (which is pretty slow to move) increasing scrupulously the speed in `drive()`.
The code could also be made computationally less demanding increasing the value of the `seconds` parameter (passed to the function `drive()` e.g. ) to raise the duration of the `sleep function` in order to compute cycles fewer times, while having the same result.
Another issue could be presented if the silver boxes are moved too close to a wall. Since the robot can see through it, it's gonna grab it without avoiding the wall. This actually never happened to me and it could be avoided with a good calibration of the function `grab_and_turn` (or with a different approach), so that a silver token is never to be found next to a wall.
Moreover could be interesting to add new feature and new functionalities to the class Robot(), in order for example to make the robot not able to see silver tokens through walls, which would probably could be a more "real" situation. 



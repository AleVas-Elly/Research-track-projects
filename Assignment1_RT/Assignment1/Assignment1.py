from __future__ import print_function
import time
from sr.robot import *

#--------------------------------------------------------------------
#The aim of the program is to make the robot run in the circuit counter 
#clock-wise without touching the walls and moving every silver token
#it sees behind it.
#
#Run with:
#	$ python run.py exercise1.py
#--------------------------------------------------------------------
#
a_th = 2.0 #float: Threshold for the control of the orientation

d_th = 0.4 #float: Threshold for the control of the linear distance

R = Robot() #instance of the class Robot

range_silver = 1.5 #float: range within the robot can see a silver token
turning_angle = 12 #float: angle of which the robot turns when sees a golden token too near 
add_to_range = 0 #float: used in the function widen_range to widen the range
Range = 1.2 #range of view of the robot for golden tokens(to be understand in wich_direction())

def drive(speed, seconds): #Function for setting a linear velocity
    
    #Arguments: speed (int): the speed of the wheels
	#  	  		seconds (int): the time interval
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds): #Function for setting an angular velocity
    
    #Args: speed (int): the speed of the wheels
	#	   seconds (int): the time interval
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token(): #Function to find the closest silver token in circol of ray = range_silver
    
    #Returns: dist (float): distance of the closest silver token (-1 if no silver token is detected)
	#		 rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    
    dist = range_silver #forse unidea per renderlo piu' preciso potrebber essere aumentare sto numero
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER: #I consider only the silver tokens inside the circle of r=dist
			dist = token.dist
			rot_y=token.rot_y 
    if dist == range_silver or ((rot_y < -45) or (rot_y > 45)): #silver token behind the robot are not taken into account, therefore it's like
																#they are not there
		return -1, -1 #the robot hasn't seen any silver token in the neighbourhood
    else:
   		return dist, rot_y  #the robot has seen at least one silver token in the neighbouthood and the closest is at a linear distance = dist
							# and at an angle of rot_t 
   	
def grab_and_turn(): #Funcion to movw the silver token behind the robot
	
	R.grab() #it grabs the token
	turn(60,1) #it turns 180deg
	R.release() #it releases the token
	drive(-10, 2) #it drives a bit backwards in order not to hit the token that has just been moved during the turn.
	turn(-60,1) #it turns again facing now the same direction it was facing before
	print ('Done!')
	
def widen_range(): #the function is needed when the robot doesn't know where to turn towards because nDx = nDy. Recursive function.
	
	global add_to_range
	nSx_w = 0  
	nDx_w = 0
	add_to_range = add_to_range + 0.1 # prima era 0.3#mult factor in order to broaden the range at every iteration
	new_Range = add_to_range + Range
	fov = 10 #float: used to modify the field of view
	for token in R.see():
		if token.dist < new_Range and (((90 - fov/2) < token.rot_y < (90 + fov/2)) or (-(90 - fov/2) > token.rot_y > -(90 + fov/2))) and token.info.marker_type is (MARKER_TOKEN_GOLD or MARKER_ARENA):
			if token.rot_y < 0: 
				nSx_w = nSx_w + 1 
			elif token.rot_y > 0: 
				nDx_w = nDx_w + 1
	if nDx_w < nSx_w:
		print ('WR-Danger! Turning right a bit...')
		print('nDx_w: ', nDx_w, ' - nSx_w: ', nSx_w )
		turn (+turning_angle, 1)
	elif nDx_w > nSx_w:
		print ('WR-Danger! Turning left a bit...') 
		print('nDx_w: ', nDx_w, ' - nSx_w: ', nSx_w )
		turn (-turning_angle, 1)
	else:
		widen_range()	#the function recursively calls itself if nDx_w = nSx_w
	
def which_direction():  #Function to make the robot turn the "right" direction (left or right) when it encounters a wall
	
	nSx = 0 #number of golden or arena blocks seen on the left of the robot 
	nDx = 0 #number of golden or arena blocks seen on the right of the robot  
	for token in R.see():
		if token.dist < Range and token.info.marker_type is (MARKER_TOKEN_GOLD or MARKER_ARENA):
			if token.rot_y < 0: 
				nSx = nSx + 1 
			elif token.rot_y > 0: 
				nDx = nDx + 1
	if nDx < nSx:
		print ('Danger! Turning right a bit...')
		turn (+turning_angle, 1)
	elif nDx > nSx:
		print ('Danger! Turning left a bit...') 
		turn (-turning_angle, 1)
	else:	#if the nDx = nSy, i have to widen a bit my range of view
		widen_range()
	add_to_range = 1
	print('numero di blocchi a dx: ', nDx, ' - numero di blocchi a sx: ', nSx )
	


def avoid_walls(): #Function to avoid walls 
	
	max_proximity = 0.7 #threshold, if a gold or arena token is found at a distance < max_proximity it's gonna start the turning procedure
	angle_of_view = 50
	for token in R.see():
		if token.dist < max_proximity and (-angle_of_view < token.rot_y < angle_of_view) and token.info.marker_type is (MARKER_TOKEN_GOLD or MARKER_ARENA): 
		#in order to make the robot see only in a certain range of view (-5angle_of_view ,angle_of_view)
			print('choosing the right direction...')
			which_direction() #the funcition that has to compute the "right" direction is called
			return 1 
	return 0
	#the function returns 1 if there are blocks nearer than max_proximity, otherwise return 0. This isn't actually used here but it's always 
	#useful for error detecion or future development
	
#main

while 1:

	dist, rot_y = find_silver_token()
	
	if dist == -1: #so the robot hasn't seen a silver token yet
		print("I don't see any token! Let's try to go forward a bit...")
		drive(60, 0.01)
		avoid_walls()
	elif (dist < d_th): #and (-90 < rot_y < 90): # if the robot iclose to the token and the token is in front of it, it tries to grab it.
		print("Found it!")
		grab_and_turn()
	elif (-a_th <= rot_y <= a_th): # if the robot is well aligned with the token, we go forward
		print("Ah, right direction, let's go for it")
		drive(20, 0.5)
	elif (rot_y < -a_th): #change this in order to make the robot turn only if the S.token is present in a narrower f.o.v.
		print('Turn left a bit')
		turn(-2, 0.5)
	elif (rot_y > a_th): #change this in order to make the robot turn only if the S.token is present in a narrower f.o.v.
		print('Turn right a bit')
		turn(+2, 0.5)
		

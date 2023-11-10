from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

We start from the solution of the exercise 2
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py exercise3.py

"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

box_finding = True   # Set this to True if the box is grabbed

R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

        
def find_token_gold():
   
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type == MARKER_TOKEN_GOLD:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y


drive(50,4)
turn(-10,1)

for box in range(6) :

    box_finding = True
    while box_finding:  # This loop will execute for each subsequent box
        dist, rot_y = find_token_gold()
    
        if dist == -1:
            print("I don't see any more tokens. All boxes are placed!")
            turn(+10, 1)
        elif dist < d_th:
            print("Found it!")
            R.grab()  # If we are close to the token, we grab it.
            print("Gotcha!")
            turn(20, 2.5)  # Adjust robot position for the next box placement
    	    drive(27,4.8)   
            R.release()  # Release the box
            drive(-20, 1.5)
            turn(-10, 3)
            drive(20, 2)
            box_finding = False  # Box placed, exit the loop
        elif -a_th <= rot_y <= a_th:  # If the robot is well aligned with the token, move forward
            print("Ah, here we are!.")
            drive(40, 0.5)
        elif rot_y < -a_th:  # If the robot is not well aligned with the token, move left
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)



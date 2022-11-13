'''
Sean Gunther
Integrated stepper motor control from taglines and camera capture
This currently takes a picture as soon as the motor is rotated.
Eventually, all code will be part of the same body to extend the various elements and recieve transmissions
The remaining features will need to be implemented for the camera control:

Do not listen for commands unless the callsign is recognized
Assign the commands to an array, then read from the array. The commands will be demarcated with spaces
C3—Take picture
D4—Change camera mode from color to grayscale
E5—Change camera mode back from grayscale to color 
F6—Rotate image 180º (upside down).G7—Special effects filter (Apply any filter or image distortion you want andstate what filter or distortion was used). 
H8—Remove all filters.

'''

import cv2 #Open CV for visual identification
import numpy as np # Dependent for openCV
import picamera as picam  #necessary for running this software with the raspberry pi camera
import time # used to determine the framerate and timestamp
import RPi.GPIO as GPIO # used to operate the stepper motors
import datetime #necessary for the timestamped images

#init lines below --------------------------------------------------------------------------
camera = picam.PiCamera(resolution=(640,360)) # very important to limit the resolution at capture instead of with cv2.resize()
start_time = int(round(time.time()*1000)) #init for the starttime, disregard the first output

GPIO.setmode(GPIO.BOARD) # sets the gpio nomenclature to refer to the board locations instead of the pin names
control_pins_pan = [3,5,7,11] # pins used for camera pan servo

for pin in control_pins_pan: # this loop inits each pin in the list as an output and assigns it low
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

#init lines above--------------------------------------------------------------------------


# global vars below--------------------------------------------------------------------------
halfstep_seq = [ 
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]
'''
The above and below lists are the half step commands to turn the stepper.
It may be worth only using full steps for speed. either method will have sub-degree accuracy
512 half steps is a full rotation
half steps are 1.422 steps per degree
full steps are .711 steps per degree
60 degrees in full steps os 42.66
60 degrees in half steps is 85.33
'''
revHalfstep_seq = [
    [1,0,0,0],
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    ]

steps_per_deg = 512/360 #calculation for steps per degree
Dist = int(60*steps_per_deg) #creates the distance to travel based on degree 
#global vars above--------------------------------------------------------------------------


def capFunc():
    print('trying')
    date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    imgName = '/home/pi/Desktop/MotorCamPics/' + date + '.jpg' #this will need to be changed to represent the name of the pi we use
    camera.annotate_text = date
    camera.capture(imgName)
    print('success')
    
#main code below
Gospel = input("Command: ")
if Gospel.upper() == "A1":
    for i in range(Dist):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins_pan[pin], revHalfstep_seq[halfstep][pin])
            time.sleep(0.0025)
    capFunc()  
elif Gospel.upper() == "B2":
    for i in range(Dist):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins_pan[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.0025)
    capFunc()
    
#main code above



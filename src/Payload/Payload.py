"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
    Sean Gunther: sean.gunther@go.tarleton.edu
    Tyler Rider: tyler.rider@go.tarleton.edu
    Domanic DeVivo: domanic.devivo@go.tarleton.edu
"""

import cv2 #Open CV for visual identification
import numpy as np # Dependent for openCV
import picamera as picam  #necessary for running this software with the raspberry pi camera
import time # used to determine the framerate and timestamp
import RPi.GPIO as GPIO # used to operate the stepper motors 
import datetime #necessary for the timestamped images
from Communication import Communication
from Acceleration import Acceleration
from berryIMUSimple import BerrySimple
import functools
import subprocess
"""
TODO:
    - Add a function the process the commands from the receiver into a list of commands and then execute them accordingly

"""
class TARPayload(Communication):
    def __init__(self):
        """_summary_ : This is the constructor for the TARPayload class. It initializes the camera and the GPIO pins for the stepper motors.
        """
        super().__init__()
        self.base_alt = self.altitude
        self.camera = picam.PiCamera(resolution=(640,480)) # very important to limit the resolution at capture instead of with cv2.resize()
        self.start_time:int = int(round(time.time()*1000)) #init for the starttime, disregard the first output
        self.signalFile = '/home/trc/Desktop/Pratice Folder/test.txt' # path and file name of file that will contain recieved transmissions
        #int for stepper Mottor
        self.Dist=85 #60% time step
        GPIO.setmode(GPIO.BCM)
        self.control_pins_pan=[19,16,26,20]

        for pin in self.control_pins_pan: # this loop inits each pin in the list as an output and assigns it low
              GPIO.setup(pin, GPIO.OUT)
              GPIO.output(pin, 0)
              
        self.halfstep_seq:list = [ 
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]
        ]       
        self.revHalfstep_seq:list = [
          [1,0,0,0],
          [1,0,0,1],
          [0,0,0,1],
          [0,0,1,1],
          [0,0,1,0],
          [0,1,1,0],
          [0,1,0,0],
          [1,1,0,0],
        ]
        '''
        The above lists are the half step commands to turn the stepper.
        It is necessary to have both, we cannot iterate through the steps in reverse.
        It may be worth only using full steps for speed. either method will have sub-degree accuracy
        512 half steps is a full rotation
        half steps are 1.422 steps per degree
        full steps are .711 steps per degree
        60 degrees in full steps os 42.66
        60 degrees in half steps is 85.33
        '''
        #self.steps_per_deg:int = 512/360 #calculation for steps per degree
        #self.Dist:int = int(60*self.teps_per_deg) #creates the distance to travel based on degree 
        #global vars above--------------------------------------------------------------------------
        
        #int motor
        
    # these functions will push or pull the motor when called. will be used for both the actuator and motor. 
    def motor_push(self,forward,sleep):
        "act backwards"
        "clockwise"
        GPIO.output(forward,GPIO.HIGH)
        time.sleep(sleep)
        GPIO.output(forward,GPIO.LOW)
        
    def motor_pull(self,backwards,sleep):
        "act forward"
        "counterclockwise"
        GPIO.output(backwards,GPIO.HIGH)
        time.sleep(sleep)
        GPIO.output(backwards,GPIO.LOW)

    #this function will be called when the payload has sucfuly landed
    def land(self,method):
        #Acuator pins
        in1= 23
        in2= 22
        act_sleep=15
        #motor pins
        in3= 18
        in4= 17
        motor=act_sleep

        #setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(in3,GPIO.OUT)
        GPIO.setup(in4,GPIO.OUT)
        if method=='push':
            varm = in2
        else:
            varm = in1
        self.motor_push(varm,act_sleep)

    def captureFunction(self):
        print('[*] Trying')
        date = datetime.datetime.now().strftime('%m-%d-%Y %H.%M.%S.%f')
        data = str(date)
        date = data[0:len(data)-4]
        imgName = '/home/trc/Downloads/TARPayload/src/img/' + date + '.jpg' #this will need to be changed to represent the name of the pi we use
        self.camera.annotate_text = date
        self.camera.capture(imgName)
        print('[+] Image Captured at '+date)
        data = f'Image Captured using capture Function saved at {imgName}'
        self.log_data(data)

    def turnFunction(self):
        print('[*] Turning')
        for i in range(self.Dist):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.control_pins_pan[pin], self.halfstep_seq[halfstep][pin])
                time.sleep(0.001)
        print('[+] Turned the camera 60 degrees to the right')
        data = f'Turn camera 60 degrees to the right'
        self.log_data(data)
        
    '''
    For what its worth, function A1 and B2 might need to be changed to reflect the true direction of the motors. Im not sure how it will actually turn the camera.
    '''
    def a1Function(self):
        """_summary_ : This function will turn the camera 60 degrees to the left.
        """
        for i in range(self.Dist):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.control_pins_pan[pin], self.revHalfstep_seq[halfstep][pin])
                time.sleep(0.0025)
        print('[+] Turned the camera 60 degrees to the left ')
        data = f'[A1]- Turned the camera 60 degrees to the left'
        self.log_data(data)
    
    def b2Function(self):
        """_summary_ : This function will turn the camera 60 degrees to the right .
        """
        for i in range(self.Dist):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.control_pins_pan[pin], self.halfstep_seq[halfstep][pin])
                time.sleep(0.0025)
        print('[+] Turned the camera 60 degrees to the right and captured an image')
        data = f'[B2]- Turned the camera 60 degrees to the right'
        self.log_data(data)
        
    def c3Function(self):
        """_summary_ : This function takes a picture and saves it to the output folder"""
        data = f'[C3]-Capture Function Called'
        self.log_data(data)
        self.captureFunction()
        print('[+] Captured an image')
        
    def d4Function(self):
        """_summary_ : This function changes the camera mode from color to grayscale"""
        self.camera.color_effects = (128,128)
        print('[+] Changed camera mode from color to grayscale')
        data = f'[D4]- Changed camera mode from color to grayscale'
        self.log_data(data)
        time.sleep(2)
        
    def e5Function(self): 
        self.camera.color_effects= None
        print('[+] Changed camera mode from grayscale to color')
        data = f'[E5]- Changed camera mode from grayscale to color'
        self.log_data(data)
   
    def f6Function(self):
        """_summary_ : This function rotates the image 180 degrees"""
        self.camera.rotation = 180
        print('[+] Rotated image 180 degrees')
        data = f'[F6]- Rotated image 180 degrees'
        self.log_data(data)
    
    def g7Function(self):
        """_summary_ : This function applies a special effect filter to the image"""
        self.camera.image_effect = 'colorswap'
        print('[+] Applied the colorswap filter')
        data = f'[G7]- Applied the colorswap filter'
        self.log_data(data)
        
    def h8Function(self):
        """_summary_ : This function removes all filters from the image"""
        self.camera.image_effect = 'none'
        self.camera.color_effects= None
        self.camera.rotation=0
        print('[+] Removed all filters')
        data = f'[H8]- Removed all filters'
        self.log_data(data)
        
    @property
    def acceleration(self):
        return Acceleration().aclrt_values()

    @property
    def command_parser(self)->list[str]:
        """_summary_: This function parses the commands from the textFile that is used to note the recived commands"""
        def fit(item):
            validCommands = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8']
            if item in validCommands:
                return True
            else:
                return False

        txtFile = open(self.signalFile, 'r', encoding="utf-8")
        lines = txtFile.readlines()
        cmdHist = []
        lines.pop(0)
        for line1, line2 in zip(lines[::2], lines[1::2]):
            print(line1, line2)
            line2 = line2[1:]
            cmdHist.append((line1[13:21], line2[line2.find(":") + 1 : line2.find("{")]))

        l = [t[1] for t in cmdHist]
        mostCommonCommand = max(l, key=l.count)
        cmdList = list(mostCommonCommand.split(" "))
        cmdList = list(filter(fit, cmdList))
        return cmdList
    
    def start_reciever(self):
        cmd="rtl_fm -f 144.950M -s 22050 |multimon-ng  -t raw -a AFSK1200 -f alpha /dev/stdin >test2.txt"
        subprocess.run(cmd,shell=True)
        return True
        
    def deploy(self,cmdList):
        """_summary_ : This function takes in a string of list of commands  calls the appropriate functions to execute the commands.

        Args:
            command (str): A string of commands to be executed by the camera.
        """
        for command in cmdList:
            command = command.upper()
            if(command == 'A1'):
                self.a1Function()
            elif(command == 'B2'):
                self.b2Function()
            elif(command == 'C3'):
                self.c3Function()
            elif(command == 'D4'):
                self.d4Function()
            elif(command == 'E5'):
                self.e5Function()
            elif(command == 'F6'):
                self.f6Function()
            elif(command == 'G7'):
                self.g7Function()
            elif(command == 'H8'):
                self.h8Function()

# ===== Main Control =====
payload = TARPayload()
payload.start_reciever() 
# ALTCEIL = payload.altitude * 1.10
# 
# baseAcc = payload.acceleration
# baseAccRange = (baseAcc * 0.95, baseAcc * 1.
# 
# checkAcc = False
# checkAlt = False
# 
# 
# while True:
#     if baseAccRange[0] < payload.acceleration < baseAccRange[1] and checkAcc == False:
#         checkAcc = True
#     if baseAltRange[0] < payload.altitude < baseAltRange[1] and checkAlt == False:
#         checkAlt = True
#     if thresGRange[0] < payload.acceleration < thresGRange[1] and checkAcc2 == False:
#         checkAcc2 = True
#     if checkAcc and checkAlt and checkAcc2:
#         break
# 
# payload.land("push")

# ===========================

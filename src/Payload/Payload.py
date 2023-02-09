"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
    Sean Gunther: sean.gunther@go.tarleton.edu
    Domanic DeVivo: domanic.devivo@go.tarleton.edu
"""

import cv2 #Open CV for visual identification
import numpy as np # Dependent for openCV
import picamera as picam  #necessary for running this software with the raspberry pi camera
import time # used to determine the framerate and timestamp
import RPi.GPIO as GPIO # used to operate the stepper motors 
import datetime #necessary for the timestamped images
from Communication import Communication
"""
TODO:
    - Add a function the process the commands from the receiver into a list of commands and then execute them accordingly

"""

class TARPayload(Communication):
    def __init__(self):
        """_summary_ : This is the constructor for the TARPayload class. It initializes the camera and the GPIO pins for the stepper motors.
        """
        super().__init__() 
        self.camera = picam.PiCamera(resolution=(640,360)) # very important to limit the resolution at capture instead of with cv2.resize()
        self.start_time:int = int(round(time.time()*1000)) #init for the starttime, disregard the first output
        
        #GPIO.setmode(GPIO.BOARD) # sets the gpio nomenclature to refer to the board locations instead of the pin names
        #for pin in self.control_pins_pan: # this loop inits each pin in the list as an output and assigns it low
              #GPIO.setup(pin, GPIO.OUT)
              #GPIO.output(pin, 0)
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
        
        
    def captureFunction(self):
        print('[*] Trying')
        date = datetime.datetime.now().strftime('%m-%d-%Y %H.%M.%S')
        imgName = '/home/trc/Downloads/TARPayload/src/img/' + date + '.jpg' #this will need to be changed to represent the name of the pi we use
        self.camera.annotate_text = date
        self.camera.capture(imgName)
        print('[+] Image Captured at '+date)
        data = f'Image Captured using capture Function saved at {imgName}'
        self.log_data(data)
        
        
    # Not Tested  
    def turnFunction(self): #this function will turn the camera 60 degrees to the right
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
    # A1 Function    
  
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
        
    # C3—Take picture
 
    def c3Function(self):
        """_summary_ : This function takes a picture and saves it to the output folder"""
        data = f'[C3]-Capture Function Called'
        self.log_data(data)
        self.captureFunction()
        print('[+] Captured an image')
        
 
         
        
        
    #D4—Change camera mode from color to grayscale
    #@staticmethod
    def d4Function(self):
        """_summary_ : This function changes the camera mode from color to grayscale"""
        self.camera.color_effects = (128,128)
        print('[+] Changed camera mode from color to grayscale')
        data = f'[D4]- Changed camera mode from color to grayscale'
        self.log_data(data)
    
        
        
    #E5—Change camera mode from grayscale to color
    #@staticmethod
    def e5Function(self):
        """_summary_ : This function changes the camera mode fro        GPIO.output(pin, 0)
        self.halfstep_seq:list = [ 
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]
        ]        m grayscale to color"""
        
        self.camera.color_effects = None
        print('[+] Changed camera mode from grayscale to color')
        data = f'[E5]- Changed camera mode from grayscale to color'
        self.log_data(data)
   
        
        
    #F6—Rotate image 180º (upside down).
   
    def f6Function(self):
        """_summary_ : This function rotates the image 180 degrees"""
   
        self.camera.rotation = 180
        print('[+] Rotated image 180 degrees')
        data = f'[F6]- Rotated image 180 degrees'
        self.log_data(data)
    
    
    #G7—Special effects filter (Apply any filter or image distortion you want andstate what filter or distortion was used). 
    #@staticmethod
    def g7Function(self):
        """_summary_ : This function applies a special effect filter to the image"""
     
        self.camera.image_effect = 'colorswap'
        print('[+] Applied the colorswap filter')
        data = f'[G7]- Applied the colorswap filter'
        self.log_data(data)
        
        
    #H8—Remove all filters.
 
    def h8Function(self):
        """_summary_ : This function removes all filters from the image"""
     
        self.camera.image_effect = None
        
        print('[+] Removed all filters')
        data = f'[H8]- Removed all filters'
        self.log_data(data)
   # This function takes in a string of list of commands  calls the appropriate functions to execute the commands.
    def process_command(self,commands):
        pass
    def deploy(self,command):
        """_summary_ : This function takes in a string of list of commands  calls the appropriate functions to execute the commands.

        Args:
            command (str): A string of commands to be executed by the camera.
        """
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
    
    
#test
test = TARPayload()
print(test.altitude)
#test.__init__()
test.d4Function()
test.captureFunction()



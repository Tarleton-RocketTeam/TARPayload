"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
    Sean Gunther: sean.gunther@go.tarleton.edu
    Tyler Rider: tyler.rider@go.tarleton.edu
    Domanic DeVivo: domanic.devivo@go.tarleton.edu
"""

import cv2  # Open CV for visual identification
import numpy as np  # Dependency for openCV
import picamera as picam  # Dependency for Raspberry PI Camera
import time  # Dependecy for Timing of Various Operations
import RPi.GPIO as GPIO  # Dependency for Stepper Motors
import datetime  # Dependency for Raspberry PI Camera Operations
from Communication import Communication
from Acceleration import Acceleration
from berryIMUSimple import BerrySimple
import subprocess


class TARPayload(Communication):
    """
    The class used to control payload operations.

    Attributes
    ----------
    baseAlt : float
        A decimal value that is the altitude of the payload when the software is started.
    camera : PiCamera Object
        A object that enables easy control of the Raspberry Pi Camera.
    start_time : int
        A integer value that indicated the start time of the payload (Note: disregard the first output)
    signalFile : str
        A string that is the path to where the reciever will save the recieve radio signal.
    LED : int
        A integer value that indicates the pin used to activate the LED.
    camera.rotation : int
        A integer value to indicate how many degrees to rotate the Raspberry Pi Camera.
    motor_clock : int
        A integer value to indicate the GPIO pin to output power to.
    motor_counter : int
        A integer value to indicate the GPIO pin to output power to.
    motor_sleep : int
        A integer value to indicate how to suspend execution for the motor.
    act_pull : int
        A integer value to indicate the GPIO pin to output power to.
    act_push : int
        A integer value to indicate the GPIO pin to output power to.
    act_sleep : int
        A integer value to indicate how to suspend execution for the actuator.
    Dist : int
        A integer value to indicate how many times the step sequences will be sent to the motor. (Note: 60% time step)
    accelerationMark : int
        A integer value to indicate the number of Gs the payload will need to expierence to trigger the deployment steps.
    control_pins_pan : list
        A list of integers that indicate which pins on the Raspberry Pi will send power to pan the Raspberry Pi Camera.
    halfstep_seq : 2D list
        A 2D list of integers that indicate which how to rotate the axle in the motor.
    revHalfstep_seq : 2D list
        A 2D list of integers that indicate which how to rotate the axle in the motor.

    Methods
    -------
    motorAccuatorControl(component, pin, sleepTime)
        To control the operation of the Acctuator used in the payload's deployment
    land(self, force=True, meth="push")
        To command the payload to
    captureFunction()
    LED_lights()
    turnFunction()
    a1Function()
    b2Function()
    c3Function()
    d4Function()
    e5Function()
    f6Function()
    g7Function()
    h8Function()
    acceleration()
    command_parser()
    sqrt(x)
    gyro_stat()
    start_reciever()
    logic()
    deploy(cmdList)
    """

    def __init__(self):
        """This is the constructor for the TARPayload class. It initializes the camera and the GPIO pins for the stepper motors."""
        super().__init__()
        self.baseAlt = self.altitude
        self.camera = picam.PiCamera(resolution=(640, 480))
        self.start_time: int = int(round(time.time() * 1000))
        self.signalFile = "/home/tar/Desktop/TARPayload/src/logs/recieverLogs.txt"
        self.imgFolderPath = "/home/tar/Desktop/TARPayload/src/img/"
        self.LED = 10
        self.camera.rotation = 90
        self.motor_clock = 23
        self.motor_counter = 22
        self.motor_sleep = 4
        self.act_pull = 18
        self.act_push = 17
        self.act_sleep = 15
        self.control_pins_pan = [19, 16, 26, 20]
        self.accelerationMark = 0.005  # Set minimum acceleration condition (Note: Should be - 5)
        self.ceiling = 500  # Set ceiling to start payload deployment (Note: Should be - = self.baseAlt * 1.10])
        self.Dist = 85
        self.backupcommands=['C3', 'A1', 'D4', 'C3', 'E5', 'A1', 'G7', 'C3', 'H8', 'A1', 'F6', 'C3'] # Hardcoded Commands

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED, GPIO.OUT)
        GPIO.setup(self.motor_clock, GPIO.OUT)
        GPIO.setup(self.motor_counter, GPIO.OUT)
        GPIO.setup(self.act_pull, GPIO.OUT)
        GPIO.setup(self.act_push, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)

        # Initiates each pin in the list as an output and assigns it low.
        for pin in self.control_pins_pan:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        self.halfstep_seq: list = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
        ]
        self.revHalfstep_seq: list = [
            [1, 0, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
        ]
        self.logic()

    def motorAccuatorControl(self, component: str, pin: int, sleepTime: int):
        """Sends power to the pin and logs what components is being powered for operation.

        Parameters
        ----------
        pin : int
            The pin that is being powered to activiate a component within the payload.
        sleepTime : int
            A integer value that is used to indcate how long the software will wait to execute the next line.
        """
        self.log_data(f"[Motor Accuator Control] - Pushing " + component)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(pin, GPIO.LOW)

    def land(self, force: bool = True, meth: str = "push"):
        """Deploys actuator and motor"""
        self.log_data(f"[Land] - Starting Landing Sequence")
        self.log_data(f"[Land] - Deploying Gimbal")
        self.motorAccuatorControl("Accuator", 17, self.act_sleep)

        if force == True:
            method = self.gyro_stat()
        else:
            method = meth
        print("[Logic] - Acuator Deployed")
        self.log_data(f"[Land] - Deployment Method: {method}")

        if method == "push":
            varm = self.motor_counter
        else:
            varm = self.motor_clock
        self.log_data("[Land] - Orienting Gimbal")
        self.motorAccuatorControl("Motor", varm, self.motor_sleep)
        print("[Logic] - Motor deployed")

    def captureFunction(self):
        """Captures an image using the Raspberry Pi Camera."""
        print("[*] Trying")
        date = datetime.datetime.now().strftime("%m-%d-%Y %H.%M.%S.%f")
        data = str(date)
        date = data[0 : len(data) - 4]
        imgName = (
            self.imgFolderPath + date + ".jpg"
        )  # this will need to be changed to represent the name of the pi we use
        self.camera.annotate_text = date
        self.camera.capture(imgName)
        print("[+] Image Captured at " + date)
        data = f"Image Captured using capture Function saved at {imgName}"
        self.log_data(data)

    def LED_lights(self):
        """Sends power to LED to indicate that the software is running."""
        for x in range(5):
            GPIO.output(self.LED, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.LED, GPIO.LOW)
            time.sleep(1)

    def turnFunction(self):
        """Rotates the Raspberry Pi Camera"""
        print("[*] Turning")
        for i in range(self.Dist):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(
                        self.control_pins_pan[pin], self.halfstep_seq[halfstep][pin]
                    )
                time.sleep(0.001)
        print("[+] Turned the camera 60 degrees to the right")
        data = f"Turn camera 60 degrees to the right"
        self.log_data(data)

    def a1Function(self):
        """Rotate the Raspberry Pi Camera 60 degrees to the left."""
        for i in range(self.Dist):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(
                        self.control_pins_pan[pin], self.revHalfstep_seq[halfstep][pin]
                    )
                time.sleep(0.0025)
        print("[+] Turned the camera 60 degrees to the left ")
        data = f"[A1]- Turned the camera 60 degrees to the left"
        self.log_data(data)

    def b2Function(self):
        """Rotate the Raspberry Pi Camera 60 degrees to the right."""
        for i in range(self.Dist):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(
                        self.control_pins_pan[pin], self.halfstep_seq[halfstep][pin]
                    )
                time.sleep(0.0025)
        print("[+] Turned the camera 60 degrees to the right and captured an image")
        data = f"[B2]- Turned the camera 60 degrees to the right"
        self.log_data(data)

    def c3Function(self):
        """Calls the captureFunction()"""
        data = f"[C3]-Capture Function Called"
        self.log_data(data)
        self.captureFunction()
        print("[+] Captured an image")

    def d4Function(self):
        """Changes the camera effect from color to graysale"""
        self.camera.color_effects = (128, 128)
        print("[+] Changed camera mode from color to grayscale")
        data = f"[D4]- Changed camera mode from color to grayscale"
        self.log_data(data)
        time.sleep(2)

    def e5Function(self):
        """Changes camera mode from grayscale to color."""
        self.camera.color_effects = None
        print("[+] Changed camera mode from grayscale to color")
        data = f"[E5]- Changed camera mode from grayscale to color"
        self.log_data(data)

    def f6Function(self):
        """Rotates the image 180 degrees."""
        self.camera.rotation = 270
        print("[+] Rotated image 180 degrees")
        data = f"[F6]- Rotated image 180 degrees"
        self.log_data(data)

    def g7Function(self):
        """Applies a special effect filter to the image."""
        self.camera.image_effect = "colorswap"
        print("[+] Applied the colorswap filter")
        data = f"[G7]- Applied the colorswap filter"
        self.log_data(data)

    def h8Function(self):
        """Removes all filters from the image."""
        self.camera.image_effect = "none"
        self.camera.color_effects = None
        self.camera.rotation = 90  # 90 because camera is on its side
        print("[+] Removed all filters")
        data = f"[H8]- Removed all filters"
        self.log_data(data)

    @property
    def acceleration(self):
        """Returns payload acceleration.

        Returns
        -------
        tuple
            A tuple of the acceleration values from the BerryIMU.
        """
        return Acceleration().aclrt_values()

    def command_parser(self) -> list[str]:
        """Parses the commands from the textFile that is used to note the recived commands.

        Returns
        -------
        list[str]
            A list of strings that are the commands to execute.
        """

        def fit(item: str) -> bool:
            """Returns True or False to indicate whether or not the passed parsed command is valid.

            Parameters
            ----------
            item : str
                A string that will be checked against the list of validCommands.

            Returns
            -------
            bool
                A boolean value to inidcate whether or not the passed item is in the list of validCommands.
            """
            validCommands = [
                "A1",
                "B2",
                "C3",
                "D4",
                "E5",
                "F6",
                "G7",
                "H8",
                "a1",
                "b2",
                "c3",
                "d4",
                "e5",
                "f6",
                "g7",
                "h8",
            ]
            if item in validCommands:
                return True
            else:
                return False
        time.sleep(30)
        txtFile = open(self.signalFile, "r", encoding="utf-8")
        self.log_data(f"[Command Parser] - Read Text File")
        lines = txtFile.readlines()
        print(f"[Command Parser] - Read Lines: {lines}")
        txtFile.close()
        cmdHist = []
        lines.pop(0)
        for line1, line2 in zip(lines[::2], lines[1::2]):
            print(line1, line2)
            line2 = line2[1:]
            toAppend = (line1[13:21], line2[line2.find(":") + 1 : line2.find("{")])
            if toAppend[0] == "KQ4CTL-6" or toAppend[0] == "KI5ZFF-1":
                self.log_data(
                    f"[Command Parser] - Parsed Sender and Parsed Commands: {toAppend}"
                )
                cmdHist.append(toAppend)

        l = [t[1] for t in cmdHist]
        mostCommonCommand = max(l, key=l.count)
        cmdList = list(mostCommonCommand.split(" "))
        cmdList = list(filter(fit, cmdList))
        self.log_data(f"[Command Parser] - Sent commmand list")
        return cmdList

    def sqrt(self, x):
        """Returns the square root of the passed x numeric parameter.

        Parameters
        ----------
        x : int
            A numeric value that needs squaring.

        Returns
        -------
        int
            The square root of the passed x parameter.
        """
        return x**0.5

    def gyro_stat(self):
        """Retrieves the orientation of the of the gyroscope.

        Returns
        -------
        str
            A string that indicates which method of orientation the motor will deploy the camera.
        """
        self.log_data(f"[Gyro Stat] - Getting Gyro Status")
        vv = BerrySimple().important
        return "pull" if 90 < abs(vv[0]) < 180 else "push"

    def start_reciever(self):
        """Sends command to terminal to start RTL-SDR reciever software.

        Returns
        -------
        bool
            A boolean value to verify that the reciever was started.
        """
        self.log_data(f"[Start Reciever] - Starting Reciever")

        def kill_process(processPid: str) -> int:
            """Kills the process of the processPid parameter.

            Parameters
            ----------
            processPid : str
                A string that is the PID of the process that needs to be killed.

            Returns
            -------
            int
                A integer that inidcated that the desired process has been killed.
            """
            if processPid != None:
                cmd = "sudo kill -9 " + str(processPid)
                subprocess.run(cmd, shell=True, capture_output=True)
            return 1

        def find_process() -> str:
            """Finds the process PID for the RTL-SDR application

            Returns
            -------
            str
                A string that is the process ID for the rtl_fm application.
            """
            cmd = "sudo pidof rtl_fm"
            process = subprocess.run(cmd, shell=True, capture_output=True)
            return process.stdout.decode("utf-8")

        outcome = kill_process(find_process())
        if outcome:
            self.log_data("[Start Reciever] - Killed rtl_fm Process")

        cmd = "rtl_fm -f 144.900M -s 22050 | multimon-ng  -t raw -a AFSK1200 -f alpha /dev/stdin > " + self.signalFile
        process = subprocess.Popen(cmd, shell=True)
        time.sleep(10)
        process.terminate()
        print("[Start Reciever] - Reciever Application Closed")
 
    def backupcommands_deploy(self):
        """Backs up the commands that are currently being run.

        Returns
        """
        ## TODO: Make an arr
        self.deploy(self.backupcommands)
        
    def logic(self):
        """Payload deployment preperation."""
        self.LED_lights()
        print("[Logic] - Preassure Reading:", self.pressure)
        print("[Logic] - Starting Altitude:", self.baseAlt, "cieling ALT:", self.ceiling, "\n")
        rstate = False
        self.log_data("[Logic] - Payload System Start")
        self.log_data(
            f"[Logic] - Starting Altitude: {self.baseAlt}, Ceiling: {self.ceiling}"
        )
        while True:
            Curent_ACC = self.acceleration
            print(f"[Logic] - Current Acceleration: {Curent_ACC}")
            Curent_ALT = self.altitude
            ACCx = Curent_ACC[0]
            ACCy = Curent_ACC[1]
            ACCz = Curent_ACC[2]
            if abs(ACCy) > self.accelerationMark:  # self.accelerationMark
                break

        while True:
            time.sleep(5)
            print("[Logic] - Curent Altitude: ", Curent_ALT)
            if Curent_ALT < self.ceiling:
                print("[Logic] - Rocket Below Ceiling")
                self.log_data("[Logic] - Ceiling Check Met")
                Curent_ACC = self.acceleration
                ACCx = Curent_ACC[0]
                ACCy = Curent_ACC[1]
                ACCz = Curent_ACC[2]
                if ACCx < 1.2 and ACCy < 1.2 and ACCz < 1.2:
                    print("[Logic] - Rocket Acceleration Low")
                    self.log_data("[Logic] - Stand still Check Met")
                    time.sleep(5)
                    self.log_data("[Logic] - 30 Second Wait Done")
                    self.land()
                    try:
                        self.start_reciever()
                        f = open(self.signalFile, "r")
                        size = len(f.readlines())
                        f.close()
                        while size <= 2:
                            f = open(self.signalFile, "r")
                            print(f"[Logic] - Length of Reciever Log File: {size}")
                            size = len(f.readlines())
                            f.close()
                            self.start_reciever()
                    except:
                        self.backupcommands_deploy()
                    break
                
                        
        self.log_data(f"[Logic] - Commands Parsed... Sending Commands!")
        self.deploy(self.command_parser())

    def deploy(self, cmdList: list[str]):
        """Takes in a list of commands and calls the appropriate functions to execute the commands.

        Parameters
        ----------
            cmdList : list[str]
                A string of commands to be executed by the camera.
        """
        for command in cmdList:
            command = command.upper()
            if command == "A1":
                self.a1Function()
            elif command == "B2":
                self.b2Function()
            elif command == "C3":
                self.c3Function()
            elif command == "D4":
                self.d4Function()
            elif command == "E5":
                self.e5Function()
            elif command == "F6":
                self.f6Function()
            elif command == "G7":
                self.g7Function()
            elif command == "H8":
                self.h8Function()


# ===== Main Control =====
if __name__ == "__main__":
    TARPayload()

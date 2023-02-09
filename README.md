# Payload Source Code for NASA USLI'23.

### Payload Python Module located in ```sh ./src/Payload```
### Install preliminary Libraries
```$ python3 -m pip install -r ./src/requirements.txt```
#### Test Code located in ```sh ./src/tests/test.py```

The Payload system that utilizes a Raspberry Pi camera and stepper motors to capture and rotate an image. It is written in Python and makes use of several libraries including OpenCV (cv2), NumPy (np), picamera, time, and RPi.GPIO.

The payload system is controlled through the TARPayload class, which is initialized with the constructor method __init__. In this method, the camera is set up with a specific resolution and the GPIO pins for the stepper motors are also initialized. The code also defines several lists of control values for the stepper motors, which will be used later to control their movement.

The payload system has two main functions: captureFunction and turnFunction. The captureFunction method uses the Raspberry Pi camera to capture an image, adds a timestamp to the image as an annotation, and saves the image with a timestamped file name. The turnFunction method uses the control values for the stepper motors to rotate the payload system by a specified number of degrees.
 


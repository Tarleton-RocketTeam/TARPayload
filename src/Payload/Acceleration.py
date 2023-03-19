#from lib.IMU import *
#import lib.IMU as IMU
import IMU
class Acceleration:
    def __init__(self):
        IMU.detectIMU()     #Detect if BerryIMU is connected.
        if(IMU.BerryIMUversion == 99):
            print(" No BerryIMU found... exiting ")
            sys.exit()
        IMU.initIMU()
    def aclrt_values(self):
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        #print("##### X = %fm/s^2  ##### Y =   %fm/s^2  ##### Z =  %fm/s^2  #####\n" % ( ACCx, ACCy,ACCz ))
        yG = (ACCx * 0.244)/1000
        xG = (ACCy * 0.244)/1000
        zG = (ACCz * 0.244)/1000
        return ( yG, xG, zG)
 



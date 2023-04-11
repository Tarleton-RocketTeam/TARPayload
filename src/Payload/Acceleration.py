import IMU
import sys


class Acceleration:
    """
    A class to calculate the acceleration read from the BerryIMU

    Methods
    -------
    aclrt_values(self)
        Used to convert the read acceleration into G's
    """

    def __init__(self):
        IMU.detectIMU()  # Detect if BerryIMU is connected.
        if IMU.BerryIMUversion == 99:
            print(" No BerryIMU found... exiting ")
            sys.exit()
        IMU.initIMU()

    def aclrt_values(self):
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        yG = (ACCx * 0.244) / 1000
        xG = (ACCy * 0.244) / 1000
        zG = (ACCz * 0.244) / 1000
        return (yG, xG, zG)

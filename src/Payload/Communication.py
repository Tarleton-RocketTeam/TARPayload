"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
    Domanic DeVivo: domanic.devivo@go.tarleton.edu
"""

from bmp388 import BMP388
from Acceleration import Acceleration
from Log import Log

class Communication(BMP388,Log,Acceleration):
    def __init__(self):
        super().__init__() 
        self.temperature, self.pressure, self.altitude = self.get_temperature_and_pressure_and_altitude()
        self.temperature, self.pressure, self.altitude = self.temperature/100.0, self.pressure/100.0, self.altitude/100.0
        #(self.yG ,self.xG ,self.zG) ,self.acceleration=self.aclrt_values(),self.aclrt_values()
        
#comms = Communication()
#comms.log_data('sss')
#print(comms.altitude)
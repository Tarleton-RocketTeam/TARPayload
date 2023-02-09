"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
"""
from lib.bmp388 import BMP388
from Log import Log

class Communication(BMP388,Log):
    def __init__(self):
        super().__init__() 
        self.temperature, self.pressure, self.altitude = self.get_temperature_and_pressure_and_altitude()
        self.temperature, self.pressure, self.altitude = self.temperature/100.0, self.pressure/100.0, self.altitude/100.0
#comms = Communication()
#comms.log_data('sss')
#print(comms.altitude)
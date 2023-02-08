from ..lib.bmp388 import BMP388


class Communication(BMP388):
    def __init__(self):
        super().init()
        self.temperature, self.pressure, self.altitude = self.get_temperature_and_pressure_and_altitude()
        self.temperature, self.pressure, self.altitude = self.temperature/100.0, self.pressure/100.0, self.altitude/100.0
     

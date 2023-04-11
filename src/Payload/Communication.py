"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
    Domanic DeVivo: domanic.devivo@go.tarleton.edu
    Tyler Rider: tyler.rider@go.tarleton.edu
"""

from bmp388 import BMP388
from Acceleration import Acceleration
from Log import Log


class Communication(BMP388, Log, Acceleration):
    """
    A class used to get the pressure and altitude from the BerryIMU

    Attirbutes
    ----------
    temperature : float
        A float value used to indicate the current temperature being read from the BerryIMU
    pressure : float
        A float value used ot inidcate the current preassure being read from teh BerryIMU
    altitude : float
        A float value used to indicate the current altitude being calculated by the bmp388.py file
    """

    def __init__(self):
        super().__init__()
        (
            self.temperature,
            self.pressure,
            self.altitude,
        ) = self.get_temperature_and_pressure_and_altitude()
        self.temperature, self.pressure, self.altitude = (
            self.temperature / 100.0,
            self.pressure / 100.0,
            self.altitude / 100.0,
        )

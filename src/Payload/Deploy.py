"""
    Teddy Oweh: ifechukwudeni.oweh@go.tarleton.edu
"""

from Payload import TARPayload
import time
system = TARPayload()

if __name__ == '__main__':
    top_base = system.base_alt+0.5
    system.log_data(f'Base Altitude - {system.base_alt} | Top Base Altitude - {top_base}')
    system.sequence('push')
    system.sequence('pull')

    #while True:
    #    if all(val <2 for val in  system.acceleration):
    #        system.log_data(f'Acceleration reached threshold [{system.acceleration[1]}YG] - ({system.acceleration})')
     #       time.sleep(30)
            
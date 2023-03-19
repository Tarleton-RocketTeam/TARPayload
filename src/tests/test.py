# Path: src/tests/test.py

from ..Payload import TARPayload

system = TARPayload()

if __name__ == '__main__':
    top_base = system.base_alt+0.5
    while True:
        if system.acceleration[1] >5:
            system.log_data(f'Acceleration reached threshold [{system.acceleration[1]}YG] - ({system.acceleration})')
            
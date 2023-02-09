# Path: src/tests/test.py

from ..Payload import TARPayload

system = TARPayload()

if __name__ == '__main__':
    command = input("Command: ")
    system.deploy(command)
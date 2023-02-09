from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='TARPayload',
    version='1.0',
    description='This is the constructor for the TARPayload class. It initializes the camera and the GPIO pins for the stepper motors',
    author='Tarleton Rocket Club',
    install_requires=required,
)
# Author: Dylan Coffey (18251382)
# Project: IoTumble (Final Year Project)
# Course: Cyber Security and IT Forensics
# University: University of Limerick (Ireland)

"""
This module contains the code to initialise the IoTumble device, connect it to AWS, start an
infinite while loop, and begin reading its accelerometer values.
"""
from raspberrypi.device import Device

if __name__ == "__main__":
    device = Device()
    device.connect()

    while True:
        device.read_accelerometer()

# Author: Dylan Coffey (18251382)
# Project: IoTumble (Final Year Project)
# Course: Cyber Security and IT Forensics
# University: University of Limerick (Ireland)

"""
This module contains the code to initialise the IoTumble program and interface with the
HomeController.
"""
from iotumble.controllers.home_controller import HomeController

if __name__ == "__main__":
    controller = HomeController()
    controller.main()

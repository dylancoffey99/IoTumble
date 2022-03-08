"""
This module contains the code to initialise the IoTumble program and interface with the
HomeController.
"""
from iotumble.controllers.home_controller import HomeController

if __name__ == "__main__":
    controller = HomeController()
    controller.main()

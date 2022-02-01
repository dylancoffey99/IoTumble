from configparser import ConfigParser

from iotumble.controllers.home_controller import HomeController

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    controller = HomeController(config)
    controller.main()

from iotumble.controllers.abstract_controller import AbstractController
from iotumble.models.session import Session


class HomeController(AbstractController):
    def __init__(self, config):
        self.home_view = self.load_view("Home")
        self.session = Session(config.get("config", "access_key_id"),
                               config.get("config", "secret_access_key"),
                               config.get("config", "region_name"))

    def main(self):
        self.home_view(self).start()

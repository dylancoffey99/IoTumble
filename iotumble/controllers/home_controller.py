from iotumble.controllers.abstract_controller import AbstractController
from iotumble.models.session import Session


class HomeController(AbstractController):
    def __init__(self, config):
        self.home_view = self.load_view("Home")(self)
        self.session = Session(config.get("config", "access_key_id"),
                               config.get("config", "secret_access_key"),
                               config.get("config", "region_name"))

    def view(self):
        self.home_view.hide()
        incident_controller = self.load_controller("Incident")(self.home_view)
        incident_controller.main()

    def main(self):
        self.home_view.start()

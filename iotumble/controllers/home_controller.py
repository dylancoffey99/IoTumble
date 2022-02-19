from iotumble.controllers.abstract_controller import AbstractController
from iotumble.models.session import Session


class HomeController(AbstractController):
    def __init__(self):
        self.home_view = self.load_view("Home")(self)
        self.fill_inputs()
        self.session = Session()

    def connect(self, access_key_id, secret_access_key, region_name):
        self.session.connect(access_key_id, secret_access_key, region_name)
        self.session.create_table("iotumble_incidents")
        self.fill_incidents()

    def disconnect(self):
        self.session.disconnect()

    def fill_inputs(self):
        config_path = "config"
        if not self.check_path(f"{config_path}.ini"):
            self.create_path(config_path)
        config = self.read_config()
        self.home_view.fill_inputs(config.get(config_path, "access_key_id"),
                                   config.get(config_path, "secret_access_key"),
                                   config.get(config_path, "region_name"))

    def fill_incidents(self):
        incident_count = self.session.request_incident_count()
        self.home_view.fill_incidents(incident_count)

    def switch(self, incident_id):
        self.home_view.hide()
        incident = self.session.request_incident(incident_id)
        incident_controller = self.load_controller("Incident")(self.home_view, incident)
        incident_controller.main()

    def main(self):
        self.home_view.start()

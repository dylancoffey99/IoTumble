from iotumble.controllers.abstract_controller import AbstractController
from iotumble.models.session import Session


class HomeController(AbstractController):
    def __init__(self, config):
        self.home_view = self.load_view("Home")(self)
        self.home_view.fill_input(config.get("config", "access_key_id"),
                                  config.get("config", "secret_access_key"),
                                  config.get("config", "region_name"))
        self.session = Session()

    def connect_session(self):
        if self.session.check_boto_session():
            home_input = self.home_view.get_input()
            self.session.connect(home_input[0], home_input[1], home_input[2])
            self.session.create_table("iotumble_incidents")
            self.fill_incidents()

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

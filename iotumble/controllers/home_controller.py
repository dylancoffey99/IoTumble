from iotumble.controllers.abstract_controller import AbstractController
from iotumble.models.session import Session


class HomeController(AbstractController):
    def __init__(self):
        self.home_view = self.load_view("Home")(self)
        self.fill_inputs()
        self.session = Session()

    def connect(self, access_key_id, secret_access_key, region_name):
        if access_key_id == "" or secret_access_key == "" or region_name == "":
            self.home_view.show_message("Please fill all the session entries!")
            return False
        self.session.connect(access_key_id, secret_access_key, region_name)
        self.session.create_table("iotumble_incidents")
        return self.fill_incidents()

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
        if not incident_count:
            self.home_view.show_message("The entered session access keys are not valid!")
            return False
        self.home_view.fill_incidents(incident_count)
        return True

    def switch(self, incident_id):
        incident = self.session.request_incident(incident_id)
        if not incident:
            self.home_view.show_message("The selected incident does not exist!")
        else:
            self.home_view.hide()
            incident_controller = self.load_controller("Incident")(self.home_view, incident)
            incident_controller.main()

    def main(self):
        self.home_view.start()

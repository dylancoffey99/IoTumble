from iotumble.controllers.abstract_controller import AbstractController


class IncidentController(AbstractController):
    def __init__(self, home_view):
        self.home_view = home_view
        self.incident_view = self.load_view("Incident")(self)

    def back(self):
        self.incident_view.close()
        self.home_view.open(self.home_view)

    def main(self):
        self.incident_view.start()

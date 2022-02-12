from iotumble.controllers.abstract_controller import AbstractController


class IncidentController(AbstractController):
    def __init__(self, home_view, incident):
        self.home_view = home_view
        self.incident = incident
        self.incident_view = self.load_view("Incident")(self)

    def fill_details(self):
        timestamp = self.incident.get_incident_timestamp()
        timestamps = self.incident.get_timestamps()
        timestamp_data = [timestamp.get_date_time(), timestamp.get_x_acc(),
                          timestamp.get_y_acc(), timestamp.get_z_acc(),
                          timestamp.get_svm()]
        self.incident_view.fill_details_labels(timestamp_data)
        self.incident_view.fill_details_tree_view(timestamps)

    def back(self):
        self.incident_view.close()
        self.home_view.open(self.home_view)

    def main(self):
        self.incident_view.start()

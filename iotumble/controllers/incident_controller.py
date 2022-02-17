from iotumble.controllers.abstract_controller import AbstractController


class IncidentController(AbstractController):
    def __init__(self, home_view, incident):
        self.home_view = home_view
        self.incident = incident
        self.incident_view = self.load_view("Incident")(self)

    def fill_details(self):
        timestamp = self.incident.get_max_timestamp()
        timestamps = self.incident.get_timestamps()
        self.incident_view.fill_details_labels(timestamp)
        self.incident_view.fill_details_tree_view(timestamps)

    def fill_graph(self, selected_graph):
        time = self.incident.get_timestamps_time()
        colors = self.incident_view.get_graph_colors()
        if selected_graph == "All Acceleration":
            timestamps_data = [self.incident.get_timestamps_x(), self.incident.get_timestamps_y(),
                               self.incident.get_timestamps_z()]
            for i, data in enumerate(timestamps_data):
                self.incident_view.plot_graph(time, data, colors[i])
        else:
            if selected_graph == "X-Acceleration":
                data = self.incident.get_timestamps_x()
            elif selected_graph == "Y-Acceleration":
                data = self.incident.get_timestamps_y()
            elif selected_graph == "Z-Acceleration":
                data = self.incident.get_timestamps_z()
            else:
                data = self.incident.get_timestamps_svm()
            self.incident_view.plot_graph(time, data, colors[2])
        self.incident_view.set_graph(time, selected_graph)

    def back(self):
        self.incident_view.close(self.incident_view)
        self.home_view.open(self.home_view)

    def main(self):
        self.incident_view.start()

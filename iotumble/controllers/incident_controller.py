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

    def export_csv(self):
        csv_path = self.join_path("exports", "csv")
        if not self.check_path(csv_path):
            self.create_path(csv_path)
        incident_id = self.incident.get_incident_id()
        file_path = self.join_path(csv_path, f"Incident {incident_id} - Timestamps")
        self.incident.export_timestamps(file_path)
        self.home_view.show_message(f"Successfully exported incident:\n'{file_path}.csv'.")

    def export_graph(self, selected_graph):
        if selected_graph == "":
            self.home_view.show_message("Please select a graph to export!")
        else:
            graph_path = self.join_path("exports", "graphs")
            if not self.check_path(graph_path):
                self.create_path(graph_path)
            incident_id = self.incident.get_incident_id()
            file_path = self.join_path(graph_path, f"Incident {incident_id} - {selected_graph}")
            self.incident_view.export_graph(file_path)
            self.home_view.show_message(f"Successfully exported graph:\n'{file_path}.png'.")

    def back(self):
        self.incident_view.close(self.incident_view)
        self.home_view.open(self.home_view)

    def main(self):
        self.incident_view.start()

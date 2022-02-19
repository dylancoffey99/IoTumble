from csv import writer


class Incident:
    def __init__(self, incident_id, timestamps):
        self.incident_id = incident_id
        self.timestamps = timestamps

    def get_incident_id(self):
        return self.incident_id

    def get_timestamps(self):
        return self.timestamps

    def get_timestamps_time(self):
        time = []
        for i in range(len(self.timestamps)):
            time.append(i / 10)
        return time

    def get_timestamps_x(self):
        x_data = []
        for timestamp in self.timestamps:
            x_data.append(timestamp.get_x_acc())
        return x_data

    def get_timestamps_y(self):
        y_data = []
        for timestamp in self.timestamps:
            y_data.append(timestamp.get_y_acc())
        return y_data

    def get_timestamps_z(self):
        z_data = []
        for timestamp in self.timestamps:
            z_data.append(timestamp.get_z_acc())
        return z_data

    def get_timestamps_svm(self):
        svm_data = []
        for timestamp in self.timestamps:
            svm_data.append(timestamp.get_svm())
        return svm_data

    def get_max_timestamp(self):
        max_timestamp = None
        max_svm = max(timestamp.get_svm() for timestamp in self.timestamps)
        for timestamp in self.timestamps:
            if timestamp.get_svm() == max_svm:
                max_timestamp = timestamp
        return max_timestamp

    def export_timestamps(self, csv_path):
        with open(f"{csv_path}.csv", "w", newline="", encoding="utf-8") as file:
            csv = writer(file, delimiter=",")
            csv.writerow(["Timestamp ID", "Timestamp", "X-Acceleration", "Y-Acceleration",
                          "Z-Acceleration", "Signal Vector Magnitude"])
            for timestamp in self.timestamps:
                csv.writerow([str(timestamp.get_timestamp_id()), timestamp.get_time(),
                              str(timestamp.get_x_acc()), str(timestamp.get_y_acc()),
                              str(timestamp.get_z_acc()), str(timestamp.get_svm())])

"""This module contains the Incident class, to represent a model of an incident."""
from csv import writer
from typing import List


class Incident:
    """
    This class represents a model of an incident. It contains a constructor, the getter methods for
    its parameters, and a CSV exporting method.
    """

    def __init__(self, incident_id: int, timestamps: List):
        """
        This constructor instantiates an Incident object.

        :param incident_id: ID of the Incident.
        :param timestamps: List of Timestamp objects.
        """
        self.incident_id = incident_id
        self.timestamps = timestamps

    def get_incident_id(self) -> int:
        """
        This method gets the Incident ID.

        :returns: ID of the Incident.
        """
        return self.incident_id

    def get_timestamps(self) -> List:
        """
        This method gets the list of Timestamp objects.

        :returns: List of Timestamp objects.
        """
        return self.timestamps

    def get_timestamps_time(self) -> List[float]:
        """
        This method gets a list of the timestamps time-data.

        :returns: List of timestamps time-data.
        """
        time = []
        for i in range(len(self.timestamps)):
            time.append(i / 10)
        return time

    def get_timestamps_x(self) -> List[float]:
        """
        This method gets a list of the timestamps x-data.

        :returns: List of timestamps x-data.
        """
        x_data = []
        for timestamp in self.timestamps:
            x_data.append(timestamp.get_x_acc())
        return x_data

    def get_timestamps_y(self) -> List[float]:
        """
        This method gets a list of the timestamps y-data.

        :returns: List of timestamps y-data.
        """
        y_data = []
        for timestamp in self.timestamps:
            y_data.append(timestamp.get_y_acc())
        return y_data

    def get_timestamps_z(self) -> List[float]:
        """
        This method gets a list of the timestamps z-data.

        :returns: List of timestamps z-data.
        """
        z_data = []
        for timestamp in self.timestamps:
            z_data.append(timestamp.get_z_acc())
        return z_data

    def get_timestamps_svm(self) -> List[float]:
        """
        This method gets a list of the timestamps svm-data.

        :returns: List of timestamps svm-data.
        """
        svm_data = []
        for timestamp in self.timestamps:
            svm_data.append(timestamp.get_svm())
        return svm_data

    def get_max_timestamp(self):
        """
        This method gets the Timestamp object with the maximum SVM value.

        :returns: Timestamp object with the maximum SVM value.
        """
        max_timestamp = None
        max_svm = max(timestamp.get_svm() for timestamp in self.timestamps)
        for timestamp in self.timestamps:
            if timestamp.get_svm() == max_svm:
                max_timestamp = timestamp
        return max_timestamp

    def export_timestamps(self, csv_path: str):
        """
        This method exports all data from the list of Timestamp objects to a CSV file of a passed
        path.

        :param csv_path: Name of CSV path.
        """
        with open(f"{csv_path}.csv", "w", newline="", encoding="utf-8") as file:
            csv = writer(file, delimiter=",")
            csv.writerow(["Timestamp ID", "Timestamp", "X-Acceleration", "Y-Acceleration",
                          "Z-Acceleration", "Signal Vector Magnitude"])
            for timestamp in self.timestamps:
                csv.writerow([str(timestamp.get_timestamp_id()), timestamp.get_time(),
                              str(timestamp.get_x_acc()), str(timestamp.get_y_acc()),
                              str(timestamp.get_z_acc()), str(timestamp.get_svm())])

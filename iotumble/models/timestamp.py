"""This module contains the Timestamp class, to represent a model of a timestamp."""
from datetime import datetime
from typing import List


class Timestamp:
    """
    This class represents a model of a timestamp. It contains a constructor and the getter methods
    for its parameters.
    """

    def __init__(self, timestamp_id: int, timestamp_data: List):
        """
        This constructor instantiates a Timestamp object.

        :param timestamp_id: ID of the Timestamp.
        :param timestamp_data: List of Timestamp data.
        """
        self.timestamp_id = timestamp_id
        self.timestamp_data = timestamp_data

    def get_timestamp_id(self) -> int:
        """
        This method gets the Timestamp ID.

        :returns: ID of the Timestamp.
        """
        return self.timestamp_id

    def get_x_acc(self) -> float:
        """
        This method gets X-Acceleration of the Timestamp.

        :returns: X-Acceleration of the Timestamp.
        """
        return self.timestamp_data[0]

    def get_y_acc(self) -> float:
        """
        This method gets Y-Acceleration of the Timestamp.

        :returns: Y-Acceleration of the Timestamp.
        """
        return self.timestamp_data[1]

    def get_z_acc(self) -> float:
        """
        This method gets Z-Acceleration of the Timestamp.

        :returns: Z-Acceleration of the Timestamp.
        """
        return self.timestamp_data[2]

    def get_svm(self) -> float:
        """
        This method gets Signal Vector Magnitude of the Timestamp.

        :returns: Signal Vector Magnitude of the Timestamp.
        """
        return self.timestamp_data[3]

    def get_date(self) -> str:
        """
        This method gets date of the Timestamp.

        :returns: Date of the Timestamp.
        """
        date_time = datetime.fromtimestamp(self.timestamp_data[4])
        return date_time.strftime("%d %B %Y")

    def get_time(self) -> str:
        """
        This method gets time of the Timestamp.

        :returns: Time of the Timestamp.
        """
        time = datetime.fromtimestamp(self.timestamp_data[4])
        return time.strftime("%H:%M:%S.%f")[:-3]

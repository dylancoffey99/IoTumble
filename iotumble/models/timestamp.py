from datetime import datetime


class Timestamp:
    def __init__(self, timestamp_id, timestamp_data):
        self.timestamp_id = timestamp_id
        self.timestamp_data = timestamp_data

    def get_timestamp_id(self):
        return self.timestamp_id

    def get_x_acc(self):
        return self.timestamp_data[0]

    def get_y_acc(self):
        return self.timestamp_data[1]

    def get_z_acc(self):
        return self.timestamp_data[2]

    def get_svm(self):
        return self.timestamp_data[3]

    def get_date(self):
        date_time = datetime.fromtimestamp(self.timestamp_data[4])
        return date_time.strftime("%d | %B | %Y")

    def get_time(self):
        time = datetime.fromtimestamp(self.timestamp_data[4])
        return time.strftime("%H:%M:%S.%f")[:-3]

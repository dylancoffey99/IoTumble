class Timestamp:
    def __init__(self, timestamp, sensor_data):
        self.timestamp = timestamp
        self.sensor_data = sensor_data

    def get_timestamp(self):
        return self.timestamp

    def get_x_data(self):
        return self.sensor_data[0]

    def get_y_data(self):
        return self.sensor_data[1]

    def get_z_data(self):
        return self.sensor_data[2]

    def get_svm_data(self):
        return self.sensor_data[3]

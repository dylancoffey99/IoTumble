class Timestamp:
    def __init__(self, timestamp_id, epoch, sensor_data):
        self.timestamp_id = timestamp_id
        self.epoch = epoch
        self.sensor_data = sensor_data

    def get_timestamp_id(self):
        return self.timestamp_id

    def get_epoch(self):
        return self.get_epoch

    def get_x_acceleration(self):
        return self.sensor_data[0]

    def get_y_acceleration(self):
        return self.sensor_data[1]

    def get_z_acceleration(self):
        return self.sensor_data[2]

    def get_svm(self):
        return self.sensor_data[3]

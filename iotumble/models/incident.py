class Incident:
    def __init__(self, incident_id, timestamps):
        self.incident_id = incident_id
        self.timestamps = timestamps

    def get_incident_id(self):
        return self.incident_id

    def get_timestamps(self):
        return self.timestamps

    def get_incident_timestamp(self):
        incident_svm = max(timestamp.get_svm() for timestamp in self.timestamps)
        for timestamp in self.timestamps:
            if timestamp.get_svm() == incident_svm:
                return timestamp
        return None

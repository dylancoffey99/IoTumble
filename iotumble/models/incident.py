class Incident:
    def __init__(self, incident_id, timestamps):
        self.incident_id = incident_id
        self.timestamps = timestamps

    def __eq__(self, other):
        return self.incident_id == other.incident_id

    def get_incident_id(self):
        return self.incident_id

    def get_timestamps(self):
        return self.timestamps

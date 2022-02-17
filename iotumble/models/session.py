from boto3 import Session as BotoSession

from iotumble.models.incident import Incident
from iotumble.models.timestamp import Timestamp


class Session:
    def __init__(self):
        self.boto_session = None
        self.incidents_table = None

    def connect(self, access_key_id, secret_access_key, region_name):
        self.boto_session = BotoSession(aws_access_key_id=access_key_id,
                                        aws_secret_access_key=secret_access_key,
                                        region_name=region_name)

    def disconnect(self):
        self.boto_session = None
        self.incidents_table = None

    def create_table(self, table_name):
        dynamo_db = self.boto_session.resource("dynamodb")
        self.incidents_table = dynamo_db.Table(table_name)

    def request_incident(self, incident_id):
        response = self.incidents_table.get_item(Key={"pk": incident_id, "sk": "incident"})
        timestamps = response["Item"]["msg"]
        timestamps = dict(sorted(timestamps.items(), key=lambda d: int(d[0])))
        incident_timestamps = []
        for timestamp_id in timestamps:
            timestamp_data = []
            sensor_data = timestamps[timestamp_id]
            for data in sensor_data:
                timestamp_data.append(float(sensor_data[data]))
            timestamp = Timestamp(int(timestamp_id), timestamp_data)
            incident_timestamps.append(timestamp)
        return Incident(incident_id, incident_timestamps)

    def request_incident_count(self):
        response = self.incidents_table.get_item(Key={"pk": 0, "sk": "count"})
        count = response["Item"]["msg"]
        return int(count)

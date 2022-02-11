from boto3 import Session as BotoSession

from iotumble.models.incident import Incident
from iotumble.models.timestamp import Timestamp


class Session:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        session = BotoSession(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
        database = session.resource("dynamodb")
        self.table = database.Table("iotumble_incidents")

    def request_incident(self, incident_id):
        response = self.table.get_item(Key={"pk": incident_id, "sk": "incident"})
        incident = response["Item"]["msg"]
        incident = dict(sorted(incident.items(), key=lambda d: int(d[0])))
        timestamps = []
        for timestamp_id in incident:
            sensor_data = []
            timestamp_data = incident[timestamp_id]
            for data in timestamp_data:
                if data != "ep":
                    sensor_data.append(float(timestamp_data[data]))
            timestamp = Timestamp(int(timestamp_id), int(timestamp_data["ep"]), sensor_data)
            if timestamp not in timestamps:
                timestamps.append(timestamp)
        return Incident(incident_id, timestamps)

    def request_incident_count(self):
        response = self.table.get_item(Key={"pk": 0, "sk": "count"})
        count = response["Item"]["msg"]
        return count

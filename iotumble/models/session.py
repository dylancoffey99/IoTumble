from boto3 import Session as BotoSession
from boto3.dynamodb.conditions import Key

from iotumble.models.incident import Incident
from iotumble.models.timestamp import Timestamp


class Session:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        session = BotoSession(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
        database = session.resource("dynamodb")
        self.table = database.Table("iotumble_db")

    def request_incident(self, incident_id):
        response = self.table.query(KeyConditionExpression=Key("incident_id").eq(incident_id))
        timestamps = []
        for item in response["Items"]:
            sensor_data = []
            timestamp_data = item["timestamp_data"]
            for data in timestamp_data:
                sensor_data.append(float(timestamp_data[data]))
            timestamp = Timestamp(int(item["timestamp"]), sensor_data)
            if timestamp not in timestamps:
                timestamps.append(timestamp)
        incident = Incident(incident_id, timestamps)
        return incident

    def request_all_incidents(self):
        response = self.table.scan()
        incidents = []
        for item in response["Items"]:
            incident = self.request_incident(int(item["incident_id"]))
            if incident not in incidents:
                incidents.append(incident)
        return incidents

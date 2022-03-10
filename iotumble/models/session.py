# Author: Dylan Coffey (18251382)
# Project: IoTumble (Final Year Project)
# Course: Cyber Security and IT Forensics
# University: University of Limerick (Ireland)

"""
This module contains the Session class, representing a model of a session, and containing the
functionality to interact with AWS.
"""
from boto3 import Session as BotoSession
from botocore.exceptions import ClientError

from iotumble.models.incident import Incident
from iotumble.models.timestamp import Timestamp


class Session:
    """
    This class represents a model of a session. It contains a constructor, the methods that allow it
    to interact with AWS, and the DynamoDB request methods.
    """

    def __init__(self):
        """This constructor instantiates a Session object."""
        self.boto_session = None
        self.incidents_table = None

    def connect(self, access_key_id: str, secret_access_key: str, region_name: str):
        """
        This method connects to AWS by creating a boto3 session.

        :param access_key_id: Access Key ID of the Session.
        :param secret_access_key: Secret Access Key of the Session.
        :param region_name: Region Name of the Session.
        """
        self.boto_session = BotoSession(aws_access_key_id=access_key_id,
                                        aws_secret_access_key=secret_access_key,
                                        region_name=region_name)

    def disconnect(self):
        """
        This method disconnects from AWS by destroying the boto3 session and DynamoDB table
        resource.
        """
        self.boto_session = None
        self.incidents_table = None

    def create_table(self, table_name: str):
        """
        This method creates a DynamoDB table resource.

        :param table_name: Name of the DynamoDB table.
        """
        dynamo_db = self.boto_session.resource("dynamodb")
        self.incidents_table = dynamo_db.Table(table_name)

    def request_incident(self, incident_id: int):
        """
        This method requests an incident item from the created DynamoDB resource, creates an
        Incident object from its response, and returns it.

        :param incident_id: ID of the Incident.
        :returns: Instance of an Incident object.
        """
        try:
            response = self.incidents_table.get_item(Key={"pk": incident_id, "sk": "incident"})
            timestamps = response["Item"]["msg"]
        except KeyError:
            return False
        else:
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
        """
        This method requests the count of incident items from the created DynamoDB resource, creates
        a count value from its response, and returns it.

        :returns: Count of incident items.
        """
        try:
            response = self.incidents_table.get_item(Key={"pk": 0, "sk": "count"})
            count = response["Item"]["msg"]
        except ClientError:
            return False
        else:
            return int(count)

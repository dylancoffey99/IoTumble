from configparser import ConfigParser
from math import sqrt
from os import path
from time import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from adafruit_adxl34x import ADXL345
from board import I2C
from boto3 import client
from botocore.exceptions import ClientError


class IoTumble:
    def __init__(self):
        self.accelerometer = ADXL345(I2C())
        self.client = None
        self.mqtt_client = None
        self.timestamps = []

    def connect(self):
        credentials = self.read_credentials()
        self.client = client("dynamodb",
                             aws_access_key_id=credentials.get("access", "access_key_id"),
                             aws_secret_access_key=credentials.get("access", "secret_access_key"),
                             region_name=credentials.get("access", "region_name"))
        self.mqtt_configure(credentials)
        self.mqtt_client.connect()

    def mqtt_configure(self, credentials):
        self.mqtt_client = AWSIoTMQTTClient(credentials.get("mqtt", "iot_thing"))
        self.mqtt_client.configureEndpoint(credentials.get("mqtt", "iot_endpoint"), 8883)
        self.mqtt_client.configureCredentials(credentials.get("path", "root_ca"),
                                              credentials.get("path", "private_key"),
                                              credentials.get("path", "certificate"))
        self.mqtt_client.configureOfflinePublishQueueing(-1)
        self.mqtt_client.configureDrainingFrequency(2)
        self.mqtt_client.configureConnectDisconnectTimeout(10)
        self.mqtt_client.configureMQTTOperationTimeout(5)

    def mqtt_publish(self):
        topic = f"iotumble/incident/{self.increment_incident_count()}"
        payload = self.create_payload()
        self.mqtt_client.publish(topic, payload, 1)

    def read_accelerometer(self):
        acceleration = self.accelerometer.acceleration
        x_acc = acceleration[0]
        y_acc = acceleration[1]
        z_acc = acceleration[2]
        svm = sqrt((x_acc * x_acc) + (y_acc * y_acc) + (z_acc * z_acc))
        epoch = time()
        timestamp = {"x": x_acc, "y": y_acc, "z": z_acc, "svm": svm, "ep": epoch}
        self.record_timestamp(timestamp)

    def record_timestamp(self, timestamp):
        self.timestamps.append(timestamp)
        if len(self.timestamps) > 31:
            del self.timestamps[-1]

    def create_payload(self):
        payload = "{"
        for i, timestamp in enumerate(self.timestamps):
            payload_timestamp = f"'{i}': {timestamp}"
            if timestamp != self.timestamps[-1]:
                payload += payload_timestamp + ", "
            else:
                payload += payload_timestamp + "}"
        return payload.replace("'", '"')

    def increment_incident_count(self):
        try:
            response = self.client.get_item(TableName="iotumble_incidents",
                                            Key={"pk": {"N": "0"}, "sk": {"S": "count"}})
            count = response["Item"]["msg"]["N"]
        except ClientError as err:
            raise err
        else:
            return int(count) + 1

    @staticmethod
    def read_credentials():
        credentials = ConfigParser()
        credentials_path = path.join(".aws", "credentials.ini")
        credentials.read(credentials_path)
        return credentials

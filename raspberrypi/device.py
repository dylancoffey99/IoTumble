from configparser import ConfigParser
from math import sqrt
from os import path
from time import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from adafruit_adxl34x import ADXL345
from board import I2C
from boto3 import client
from botocore.exceptions import ClientError


class Device:
    def __init__(self):
        self.accelerometer = ADXL345(I2C())
        self.client = None
        self.mqtt_client = None
        self.incident_flag = False
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
        topic = f"iotumble/incident/{self.request_incident_count() + 1}"
        payload = self.create_payload()
        self.mqtt_client.publish(topic, payload, 1)

    def create_payload(self):
        payload = "{"
        for i, timestamp in enumerate(self.timestamps):
            payload_timestamp = f"'{i}': {timestamp}"
            if timestamp != self.timestamps[-1]:
                payload += payload_timestamp + ", "
            else:
                payload += payload_timestamp + "}"
        return payload.replace("'", '"')

    def request_incident_count(self):
        try:
            response = self.client.get_item(TableName="iotumble_incidents",
                                            Key={"pk": {"N": "0"}, "sk": {"S": "count"}})
            count = response["Item"]["msg"]["N"]
        except ClientError as err:
            raise err
        else:
            return int(count)

    def read_accelerometer(self):
        timestamp = self.create_timestamp()
        self.record_timestamp(timestamp)
        if not self.incident_flag:
            self.check_timestamp(timestamp)

    def create_timestamp(self):
        x_acc, y_acc, z_acc = self.accelerometer.acceleration
        svm = sqrt((x_acc * x_acc) + (y_acc * y_acc) + (z_acc * z_acc))
        timestamp = {"x": x_acc, "y": y_acc, "z": z_acc, "svm": svm, "ep": time()}
        return timestamp

    def record_timestamp(self, timestamp):
        self.timestamps.append(timestamp)
        if len(self.timestamps) > 31:
            self.timestamps.pop()

    def check_timestamp(self, timestamp):
        svm = timestamp.get("svm")
        if svm > 25 and svm >= self.timestamps[1].get("svm"):
            x_acc = timestamp.get("x")
            if x_acc < 0 and x_acc <= self.timestamps[1].get("x"):
                y_acc = timestamp.get("y")
                if y_acc < -15 and y_acc <= self.timestamps[1].get("y"):
                    z_acc = timestamp.get("z")
                    if z_acc > 10 and z_acc >= self.timestamps[1].get("z"):
                        self.incident_detected()

    def incident_detected(self):
        self.incident_flag = True
        for _ in range(int(len(self.timestamps) / 2)):
            self.read_accelerometer()
        self.incident_flag = False
        self.mqtt_publish()

    @staticmethod
    def read_credentials():
        credentials = ConfigParser()
        credentials_path = path.join(".aws", "credentials.ini")
        credentials.read(credentials_path)
        return credentials

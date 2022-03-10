# Author: Dylan Coffey (18251382)
# Project: IoTumble (Final Year Project)
# Course: Cyber Security and IT Forensics
# University: University of Limerick (Ireland)

"""
This module contains the Device class, containing the functionality to run the IoTumble
device.
"""
from configparser import ConfigParser
from math import sqrt
from os import path
from time import sleep, time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from adafruit_adxl34x import ADXL345
from board import I2C
from boto3 import client
from botocore.exceptions import ClientError


class Device:
    """
    This class represents the IoTumble device, containing a constructor, the methods that allow the
    device to connect and publish messages to AWS, the methods to create and record timestamps, and
    the methods to read and monitor the accelerometer for threshold limits and inactivity.
    """

    def __init__(self):
        """This constructor instantiates a Device object."""
        self.accelerometer = ADXL345(I2C())
        self.client = None
        self.mqtt_client = None
        self.threshold_flag = False
        self.timestamps = []

    def connect(self):
        """This method connects the device to AWS and AWS IoT using its read credentials.ini."""
        credentials = self.read_credentials()
        self.client = client("dynamodb",
                             aws_access_key_id=credentials.get("access", "access_key_id"),
                             aws_secret_access_key=credentials.get("access", "secret_access_key"),
                             region_name=credentials.get("access", "region_name"))
        self.mqtt_configure(credentials)
        self.mqtt_client.connect()

    def mqtt_configure(self, credentials: ConfigParser):
        """
        This method configures the devices MQTT client to publish messages to AWS IoT, using its
        read credentials.ini.

        :param credentials: ConfigParser object of the devices read credentials.ini.
        """
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
        """This method publishes a created JSON payload string to AWS IoT using the MQTT client."""
        topic = f"iotumble/incident/{self.request_incident_count() + 1}"
        payload = self.create_payload()
        self.mqtt_client.publish(topic, payload, 1)

    def create_payload(self) -> str:
        """
        This method creates a JSON payload string of the devices timestamp list.

        :returns: JSON payload string of the devices timestamps.
        """
        payload = "{"
        for i, timestamp in enumerate(self.timestamps):
            payload_timestamp = f"'{i}': {timestamp}"
            if timestamp != self.timestamps[-1]:
                payload += payload_timestamp + ", "
            else:
                payload += payload_timestamp + "}"
        return payload.replace("'", '"')

    def request_incident_count(self) -> int:
        """
        This method requests the count of incident items from the DynamoDB client, so its response
        can be incremented.

        :returns: Count of incident items.
        """
        try:
            response = self.client.get_item(TableName="iotumble_incidents",
                                            Key={"pk": {"N": "0"}, "sk": {"S": "count"}})
            count = response["Item"]["msg"]["N"]
        except ClientError as err:
            raise err
        else:
            return int(count)

    def read_accelerometer(self):
        """
        This method reads the devices accelerometer, creates and records a timestamp, and if the
        threshold flag is False, it checks if its acceleration values have reached any thresholds.
        """
        sleep(0.1)
        timestamp = self.create_timestamp()
        self.record_timestamp(timestamp)
        if not self.threshold_flag:
            self.check_thresholds(timestamp)

    def create_timestamp(self) -> dict:
        """
        This method uses the acceleration values of the devices accelerometer to calculate the
        Signal Vector Magnitude (SVM), and then create a timestamp with these values.

        :returns: Created timestamp.
        """
        x_acc, y_acc, z_acc = self.accelerometer.acceleration
        svm = self.calculate_svm(x_acc, y_acc, z_acc)
        timestamp = {"x": x_acc, "y": y_acc, "z": z_acc, "svm": svm, "ep": time()}
        return timestamp

    def record_timestamp(self, timestamp: dict):
        """
        This method records a timestamp to the devices timestamp list. It then deletes the first
        timestamp in the list if the list is larger than 51 (each timestamp is 0.1s, so only 5
        seconds of previous timestamps are saved).

        :param timestamp: Created Timestamp.
        """
        self.timestamps.append(timestamp)
        if len(self.timestamps) > 51:
            self.timestamps.pop(0)

    def check_thresholds(self, timestamp: dict):
        """
        This method checks if the absolute values of a created timestamp have reached the set
        thresholds. If its SVM reaches a value of 20, and any acceleration reaches a value of 18,
        the thresholds have been reached.

        :param timestamp: Created Timestamp.
        """
        svm = abs(timestamp.get("svm"))
        if svm > 20:
            for key in ("x", "y", "z"):
                data = abs(timestamp.get(key))
                if data > 18:
                    self.threshold_reached()
                    break

    def threshold_reached(self):
        """
        This method sets the threshold flag to True, gets the half length of the devices timestamp
        list, and reads the accelerometer for this amount of timestamps. The device then checks
        these read timestamps for inactivity, by passing half of their length to check_inactivity()
        (as the first few timestamps will still be active due to the devices impact/movement).
        """
        self.threshold_flag = True
        post_threshold_length = int(len(self.timestamps) / 2)
        for _ in range(post_threshold_length):
            self.read_accelerometer()
        self.check_inactivity(int(post_threshold_length / 2))
        self.threshold_flag = False

    def check_inactivity(self, inactivity_length: int):
        """
        This method gets lists of the absolute post threshold values, loops through each one,
        calculates their average, and checks if any value in the list is within -1 or 1 of their
        average. If all values are within this range, the device is inactive so it publishes an
        incident to AWS.

        :param inactivity_length: Length to check for inactivity.
        :return: None (if any value isn't within -1 or 1 of their average).
        """
        post_threshold = self.get_post_threshold(inactivity_length)
        for data_list in post_threshold.values():
            average = sum(data_list) / inactivity_length
            for data in data_list:
                comparison = data - average
                if -1 <= comparison <= 1:
                    continue
                return
        self.mqtt_publish()

    def get_post_threshold(self, inactivity_length: int) -> dict:
        """
        This method uses the inactivity length to get the last timestamps of its amount from the
        devices timestamp list. It then stores the absolute values for each timestamp into lists,
        and returns them in a dictionary, with their corresponding keys.

        :param inactivity_length: Length to check for inactivity.
        :return: Lists of the absolute post threshold values.
        """
        post_threshold = {"x": [], "y": [], "z": [], "svm": []}
        for timestamp in self.timestamps[-inactivity_length:]:
            for key, value in post_threshold.items():
                value.append(abs(timestamp.get(key)))
        return post_threshold

    @staticmethod
    def calculate_svm(x_acc: float, y_acc: float, z_acc: float) -> float:
        """
        This method calculates the Signal Vector Magnitude from the passed acceleration values.

        :param x_acc: X-Acceleration value.
        :param y_acc: Y-Acceleration value.
        :param z_acc: Z-Acceleration value.
        :return: Signal Vector Magnitude value.
        """
        svm = sqrt((x_acc * x_acc) + (y_acc * y_acc) + (z_acc * z_acc))
        return svm

    @staticmethod
    def read_credentials() -> ConfigParser:
        """
        This method creates and returns a ConfigParser object of the devices read credentials.ini.

        :returns: ConfigParser object of the devices read credentials.ini.
        """
        credentials = ConfigParser()
        credentials_path = path.join(".aws", "credentials.ini")
        credentials.read(credentials_path)
        return credentials

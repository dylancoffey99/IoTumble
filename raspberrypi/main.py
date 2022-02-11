from configparser import ConfigParser
from math import sqrt

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class Main:
    def __init__(self):
        self.mqtt_client = AWSIoTMQTTClient(config.get("config", "iot_thing"))

    def mqtt_connect(self):
        self.mqtt_client.configureEndpoint(config.get("config", "iot_endpoint"), 8883)
        self.mqtt_client.configureCredentials(config.get("dir", "root_ca"),
                                              config.get("dir", "private_key"),
                                              config.get("dir", "certificate"))
        self.mqtt_client.configureOfflinePublishQueueing(-1)
        self.mqtt_client.configureDrainingFrequency(2)
        self.mqtt_client.configureConnectDisconnectTimeout(10)
        self.mqtt_client.configureMQTTOperationTimeout(5)
        self.mqtt_client.connect()

    def mqtt_publish(self, incident_id, incident_data):
        topic = "iotumble/incident/" + str(incident_id)
        payload = "{"
        for i, data in enumerate(incident_data):
            x_acc = data[0]
            y_acc = data[1]
            z_acc = data[2]
            epoch = data[3]
            svm = sqrt((x_acc * x_acc) + (y_acc * y_acc) + (z_acc * z_acc))
            timestamp_data = "'" + str(i) + "': " + str({"x": x_acc, "y": y_acc, "z": z_acc,
                                                         "svm": svm, "ep": epoch})
            if data != incident_data[-1]:
                payload += timestamp_data + ", "
            else:
                payload += timestamp_data + "}"
        payload = payload.replace("'", '"')
        self.mqtt_client.publish(topic, payload, 1)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    main = Main()
    main.mqtt_connect()

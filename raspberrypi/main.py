from configparser import ConfigParser
from math import sqrt

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class Main:
    def __init__(self, pi_config):
        self.pi_config = pi_config
        self.mqtt_client = AWSIoTMQTTClient(pi_config.get("config", "iot_thing"))

    def mqtt_connect(self):
        self.mqtt_client.configureEndpoint(self.pi_config.get("config", "iot_endpoint"), 8883)
        self.mqtt_client.configureCredentials(self.pi_config.get("dir", "root_ca"),
                                              self.pi_config.get("dir", "private_key"),
                                              self.pi_config.get("dir", "certificate"))
        self.mqtt_client.configureOfflinePublishQueueing(-1)
        self.mqtt_client.configureDrainingFrequency(2)
        self.mqtt_client.configureConnectDisconnectTimeout(10)
        self.mqtt_client.configureMQTTOperationTimeout(5)
        self.mqtt_client.connect()

    def mqtt_publish(self, incident_id, x, y, z):
        topic = "iotumble/incidents/" + str(incident_id) + "/data"
        svm = sqrt((x * x) + (y * y) + (z * z))
        payload = "{\"x\":\"" + str(x) + "\",\"y\":\"" + str(y) + "\",\"z\":\"" \
                  + str(z) + "\",\"svm\":\"" + str(svm) + "\"}"
        self.mqtt_client.publish(topic, payload, 1)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    main = Main(config)
    main.mqtt_connect()
    main.mqtt_publish(1, -4.887451171881, -7.242191473517, 3.438523905867)

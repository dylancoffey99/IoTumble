from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

iot_thing = "raspberrypi"
iot_endpoint = "a2f51vytpcqhsx-ats.iot.us-east-1.amazonaws.com"
certs_path = "/home/pi/IoTumble/raspberrypi/certs/"
cert_auth = certs_path + "root-ca.pem"
pvt_key = certs_path + "private.pem.key"
cert = certs_path + "certificate.pem.crt"

myMQTTClient = AWSIoTMQTTClient(iot_thing)
myMQTTClient.configureEndpoint(iot_endpoint, 8883)
myMQTTClient.configureCredentials(cert_auth, pvt_key, cert)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()

timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
message = "Testing MQTT message publishing!"
payload = "{\"device\":\"" + iot_thing + "\",\"message\":\"" + message + \
          "\",\"timestamp\":\"" + timestamp + "\"}"
myMQTTClient.publish(iot_thing, payload, 1)

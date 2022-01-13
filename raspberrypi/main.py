from math import sqrt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

iot_thing = "raspberrypi"
iot_endpoint = "a2f51vytpcqhsx-ats.iot.us-east-1.amazonaws.com"
certs_path = "certs/"
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

x = -4.887451171881
y = -7.242191473517
z = 3.438523905867
svm = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))

topic = iot_thing + "/accelerometer/data"
payload = "{\"x\":\"" + str(x) + "\",\"y\":\"" + str(y) + "\",\"z\":\"" \
          + str(z) + "\",\"svm\":\"" + str(svm) + "\"}"
myMQTTClient.publish(topic, payload, 1)

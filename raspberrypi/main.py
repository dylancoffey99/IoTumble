from iotumble import IoTumble

if __name__ == "__main__":
    iotumble = IoTumble()
    iotumble.connect()

    while True:
        iotumble.read_accelerometer()

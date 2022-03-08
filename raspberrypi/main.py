from device import Device

if __name__ == "__main__":
    device = Device()
    device.connect()

    while True:
        device.read_accelerometer()

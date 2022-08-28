# IoTumble
***IoT and Fall Detection – cloud alerting, data logging and visualisation***
- Author: Dylan Coffey (18251382)
- Project: Final Year Project
- Course: Cyber Security and IT Forensics
- University: University of Limerick (Ireland)

## Requirements:
- Python 3.8+ (https://www.python.org/downloads/)
- PyCharm IDE Community Edition (https://www.jetbrains.com/pycharm/download/)
- Raspberry Pi Board interfacing with an ADXL345 Accelerometer

## Library Requirements:
- Pillow (used to display the IoTumble logo within the GUI)
- Matplotlib
- AWS SDK for Python (Boto3)
- AWS IoT Device SDK for Python
- Adafruit CircuitPython ADXL34x Driver
- CircuitPython Board

## Instructions:
### IoTumble Program:
1. To run the program, install the source code of 'iotumble' into a new project within PyCharm IDE Community Edition.
2. The following libraries must be installed using the following commands via a terminal:
```
pip install Pillow
pip install matplotlib
pip install boto3
pip install botocore
```
3. Once all libraries have been installed, run the 'main.py' file of the source code to initialise the program.

### IoTumble Device:
1. To run the device, install the source code of 'raspberrypi' to a Raspberry Pi board that interfaces with an ADXL345 accelerometer.
2. Python 3.8+ must be installed on the device.
3. The following libraries must also be installed using the following commands via a terminal:
```
pip install boto3
pip install botocore
pip install AWSIoTPythonSDK
pip install adafruit-circuitpython-adxl34x
pip install board
```
4. Once all libraries have been installed, run the 'main.py' file of the source code to initialise the device.

## Comments:
- To build the AWS architecture for IoTumble, please reference the report of this project.
- The necessary credentials to connect to AWS can been placed within the .ini files of the hidden '.aws' directories.
- AWS Free Tier can be used to build the AWS architecture for free.
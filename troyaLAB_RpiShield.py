import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import troyalab.RPi_Shield
from time import sleep     # Import the sleep function from the time module
import datetime
import json

print("Started")
troyalab = troyalab.RPi_Shield.BG96("/dev/ttyS0")
troyalab.setupGPIO()
sleep(1)
troyalab.powerUp()
sleep(1)
troyalab.sendATComm("ATE1","OK\r\n")

troyalab.getIMEI()
sleep(0.5)
troyalab.getFirmwareInfo()
sleep(0.5)
troyalab.getHardwareInfo()
sleep(5)

"""
troyalab.setGSMBand(troyalab.GSM_900) 
sleep(0.5)
troyalab.setMode(troyalab.GSM_MODE)
sleep(0.5)
"""

troyalab.connectToOperator()
sleep(2)
troyalab.getSignalQuality()
sleep(0.5)
troyalab.getQueryNetworkInfo()
sleep(0.5)

troyalab.setNetworkRegStatus()
sleep(0.5)
troyalab.setAPN("internet") #Operator APN
sleep(0.5)

troyalab.deactivateContext()
sleep(0.5)
troyalab.activateContext()
sleep(0.5)

troyalab.getAPN_IPaddress()
sleep(1)

"""
troyalab.ConnectMQTTServer("3.144.39.189","1883")
sleep(1)  # Sleep for 1 second
troyalab.MQTTDeviceConf("raspi","raspi","raspi")
sleep(1)  # Sleep for 1 second
"""

troyalab.ThingboardMQTTBasicConfig("3.144.39.189","1883","raspi","raspi","raspi")

while True:
    sleep(8)
    troyalab.publishDataMQTT("v1/devices/me/telemetry", "{\"fatih\":6,\"furkan\":34}")
    sleep(8)
    troyalab.publishDataMQTT("v1/devices/me/telemetry", "{\"fatih\":34.51,\"furkan\":6.34}")
    sleep(8)

    sensor_data = {'temperature': 0, 'humdity': 0, 'dtime': 0}
    sensor_data['temperature'] = 21
    sensor_data['humdity'] = 22
    sensor_data['dtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    troyalab.publishDataMQTT('v1/devices/me/telemetry', json.dumps(sensor_data))
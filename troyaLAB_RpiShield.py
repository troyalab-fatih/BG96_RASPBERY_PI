import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import troyalab.RPi_Shield
from time import sleep     # Import the sleep function from the time module


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
sleep(0.5)
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
sleep(0.5)


troyalab.ConnectMQTTServer("194.31.59.188","1883")
sleep(0.5)

troyalab.MQTTDeviceConf("deneme","deneme","deneme")
sleep(0.5)

troyalab.sendDataMQTT("v1/devices/me/telemetry/","{\"fatih\":6.34,\"furkan\":51.51}")
sleep(0.5)

while True:


    #troyalab.sendATComm("AT+QCFG=\"band\"","OK\r\n")
    #answer = troyalab.AT_komut_gonder("AT+CPIN?", True)
    sleep(1)

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module

import serial
from time import sleep
import time

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)

ser = serial.Serial("/dev/ttyS0", 115200)  # Open port with baud rate


def AT_komut_gonder(command):
    if (ser.isOpen() == False):
        ser.open()
    compose = ''
    compose = str(command) + "\r\n"
    ser.reset_input_buffer()
    ser.write(compose.encode())


def sendATCommOnce(command):
    if (ser.isOpen() == False):
        ser.open()
    compose = ""
    #compose = str(command) + "\r\n"
    ser.reset_input_buffer()
    ser.write(command.encode())
    sleep(0.5)
    response = ser.read_all().decode()
    sleep(1)
    print(response)


# debug_print(self.compose)
def millis():
    return int(time.time())


def sendATComm(command, desired_response, timeout=None):
    if timeout is None:
        timeout = timeout
    sendATCommOnce(command)
    f_debug = False
    timer = millis()
    while 1:
        if (millis() - timer > timeout):  # BURADA HATA VAR NONE ATAMAYLA INTEGER KIYASLIYOR
            sendATCommOnce(command)
            timer = millis()
            f_debug = False
        response = ""
        while (ser.inWaiting()):
            try:
                response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
                sleep(0.1)  # Sleep for 1 second
            except Exception as e:
                print(e.Message)
        # debug_print(self.response)
        if (response.find(desired_response) != -1):
            print(response)
            return response  # returns the response of the command as string.
            break


while True:
    # ser.write("Hello")
    # print('Bitti')

    # temp = "AT+OK\r\n"
    # ser.write(temp.encode())
    # sendATComm("AT+CSQ","OK\r\n")
    #

    #sendATCommOnce("ATI")
    sleep(2)  # Sleep for 1 second
    # sleep(2)  # Sleep for 1 second
    # AT_komut_gonder("ATE")
    #
    # GPIO.output(4, GPIO.HIGH)  # Turn on
    # sleep(1)  # Sleep for 1 second
    # GPIO.output(4, GPIO.LOW)  # Turn off
    # sleep(1)  # Sleep for 1 second

    sendATCommOnce("ATE\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(1)  #


    sendATCommOnce("ATI\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("AT+CPIN?\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("AT+CFUN=1\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("AT+COPS?\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(5)  # Sleep for 1 second

#----------------------------- IP

    sendATCommOnce("AT+CGDCONT=1,\"IP\",\"internet\"\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(4)  # Sleep for 1 second

    sendATCommOnce("AT+CREG=1\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("AT+CREG?\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("AT+CEREG?\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("AT+CGREG?\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(6)  # Sleep for 1 second

    sendATCommOnce("AT+QIACT=1\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(6)  # Sleep for 1 second

    sendATCommOnce("AT+CGPADDR\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(3)  # Sleep for 1 second

    sendATCommOnce("AT+QPING=1,\"8.8.8.8\"\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(6)  # Sleep for 1 second

#------------------------MQTT
    sendATCommOnce("AT+QMTOPEN=0,\"194.31.59.188\",1883\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(4)  # Sleep for 1 second

    sendATCommOnce("AT+QMTCONN=0,\"deneme\",\"deneme\",\"deneme\"\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(4)  # Sleep for 1 second

    sendATCommOnce("AT+QMTPUB=0,0,0,0,\"v1/devices/me/telemetry\"\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    sendATCommOnce("{\"fatih\":1.10,\"furkan\":5.65}\r\n")
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(0.05)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off
    sleep(2)  # Sleep for 1 second

    command_variable = chr(26)
    ser.write(command_variable.encode('utf-8'))
    GPIO.output(4, GPIO.HIGH)  # Turn on
    sleep(1)  # Sleep for 1 second
    GPIO.output(4, GPIO.LOW)  # Turn off

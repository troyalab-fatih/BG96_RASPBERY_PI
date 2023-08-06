import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import troyalab.RPi_Shield
from time import sleep     # Import the sleep function from the time module


print("Started")
troyalab = troyalab.RPi_Shield.BG96("/dev/ttyS0")


while True:
    #answer = troyalab.AT_komut_gonder("ATE1", True)

    troyalab.sendATComm("AT+QNWINFO","OK\r\n")
    #answer = troyalab.AT_komut_gonder("AT+CPIN?", True)
    sleep(1)

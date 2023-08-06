import time

try:
    import serial
except Exception as e:
    print("serial Library not found.")

try:
    import RPi.GPIO as GPIO
except Exception as e:
    print("GPIO Library not found.")

try:
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)+
except Exception as e:
    print("Error RPi.GPIO")

ser = serial.Serial()

#===========================================================================================================#
def millis():
    return int(time.time())


#===========================================================================================================#
class BG96:

    board          = ""  # shield name (BG96-RPi Shield)
    MQTT_BROKER_IP = ""  # MQTT IP Address
    MQTT_PORT      = 1883  # MQTT Port number #default 1883
    MQTT_CLIENT_ID = ""  # FOR MQTT
    MQTT_USER_NAME = ""  # port number
    MQTT_PASSWORD  = ""

    TIMEOUT = 2  # default timeout for function and methods on this library.
    MAX_ATTEMPT_TIME = 2
    ERROR = -1

    BG96_POWERKEY = 23
    STATUS = 10
    BG96_RESET = 22

    # GSM Bands
    GSM_NO_CHANGE = "0"
    GSM_900 = "1"  #Default #Türkiye(Turkey)
    GSM_1800 = "2"
    GSM_850 = "4"
    GSM_1900 = "8"
    GSM_ANY = "F"

    SCRAMBLE_ON = "0"
    SCRAMBLE_OFF = "1"

    # Special Characters
    CTRL_Z = '\x1A'

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    """
    def __init__(self, serial_port="/dev/ttyS0", serial_baudrate=115200, board="BG96 RPi Shield", rtscts=False, dsrdtr=False):
        try:
            if isinstance(serial_port,str):
                pass
            else:
                print("'serial_port' Value must be a string")
        except Exception as e:
            print(serial_port + " is not a valid com port." )

        self.board = board
        ser.port = serial_port
        ser.baudrate = serial_baudrate
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.bytesize = serial.EIGHTBITS
        ser.rtscts = rtscts
        ser.dsrdtr = dsrdtr

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    """
    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BG96_POWERKEY, GPIO.OUT)
        GPIO.setup(self.STATUS, GPIO.IN)

    def __del__(self):
        self.clearGPIOs()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Clearing global compose variable
    """
    def clear_compose(self):
        self.compose = ""

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Clearing GPIO's setup
    """
    def clearGPIOs(self):
        GPIO.cleanup()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Powering up BG96 module
    """
    def powerUp(self):
        GPIO.output(self.BG96_POWERKEY, 1)
        while self.getModemStatus():
            pass
        print("BG96 module powered up!")
        GPIO.output(self.BG96_POWERKEY, 0)

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Reset BG96 module
    """
    def resetBG96(self):
        GPIO.output(self.BG96_RESET, 1)
        time.sleep(0.3)
        print("BG96 module Reset")
        GPIO.output(self.BG96_RESET, 0)
        time.sleep(0.1)

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Getting modem power status
    """
    def getModemStatus(self):
        return GPIO.input(self.STATUS)

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Getting modem response
    """
    def getResponse(self, desired_response):
        if (ser.isOpen() == False):
            ser.open()
        while 1:
            self.response = ""
            while (ser.inWaiting()):
                self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
            if (self.response.find(desired_response) != -1):
                print(self.response)
                break

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # param  : (self)
    # param  : (command)
    """
    def sendATCommOnce(self, command):
        if (ser.isOpen() == False):
            ser.open()
        self.compose = ""
        self.compose = str(command) + "\r"
        ser.reset_input_buffer()
        ser.write(self.compose.encode())


    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # param  : (self)
    # param  : (command)
    # param  : (desired_response)
    # param  : (TIMEOUT)
    # param  : (MAX_ATTEMPT_TIME)
    #return  : (ERROR) , (self.response)
    """
    def sendATComm(self, command, desired_response, TIMEOUT=None , MAX_ATTEMPT_TIME=None):
        attempt_time = 0
        if TIMEOUT is None:
            TIMEOUT = self.TIMEOUT
        if MAX_ATTEMPT_TIME is None:
            MAX_ATTEMPT_TIME = self.MAX_ATTEMPT_TIME
        self.sendATCommOnce(command)
        timer = millis()
        while 1:
            if (millis() - timer > TIMEOUT):
                self.sendATCommOnce(command)
                timer = millis()
                attempt_time += 1
                if(attempt_time > MAX_ATTEMPT_TIME):
                    print("MAX ATTEMPT")
                    return self.ERROR

            self.response = ""
            while (ser.inWaiting()): # not safety kritik
                try:
                    self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
                    time.sleep(0.1)
                except Exception as e:
                    print(e.Message)

            if (self.response.find(desired_response) != -1):
                print(self.response)
                return self.response  # returns the response of the command as string.

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Saving conf. and reset BG96_AT module
    """
    def resetModule(self):
        self.saveConfigurations()
        time.sleep(0.2)
        self.resetBG96()
        self.powerUp()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Save configurations that be done in current session. 
    """
    def saveConfigurations(self):
        self.sendATComm("AT&W", "OK\r\n")







##-------------------
###OLD
    def AT_komut_gonder(self, command_user, print_response = False):
        is_OK = False
        try:
            if (ser.isOpen() == False):
                ser.open()
        except AttributeError:
            print("Serial port could not be opened")
            #return
            quit() #burayı tekrar dusunelim, uygulamadan mı cikmali yoksa return ile fonksiyondan mı cikmali
        compose = ''
        compose = str(command_user) + "\r\n"
        ser.reset_input_buffer()
        ser.write(compose.encode())
        time.sleep(.300)
        response = ser.read_all()
        size = len(response)

        if ((response[size-1] == 10) and (response[size-2] == 13) and (response[size-3] == 75) and (response[size-4] == 79)):
            is_OK = True
            print("BG96's answer is OK.")
        else:
            print("BG96's answer is not OK.")

        if(print_response == True):
            print("BG96 Response : ", end="")
            print(response.decode("utf-8"))

        return is_OK
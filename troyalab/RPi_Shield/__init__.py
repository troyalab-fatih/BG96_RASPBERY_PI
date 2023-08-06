import time

try:
    import serial
except Exception as e:
    print("serial Library not found.")

try:
    import picamera
    import RPi.GPIO as GPIO
except Exception as e:
    print("GPIO Library not found.")

try:
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)+
except Exception as e:
    print("Error RPi.GPIO")

#===========================================================================================================#

class BG96:
    def __init__(self, com_port):
        self.command = []
        self.response = []
        self.pins = []
        try:
            if isinstance(com_port,str):
                self.ser = serial.Serial(com_port, 115200)
            else:
                print("'com_port' Value must be a string")
        except Exception as e:
            print(com_port + " is not a valid com port." )
        self.baudrate = 115200

    def connect_serial(self, com_port):
        if self.baudrate != 115200:
            print("Error Baud")
        else:
            self.ser = serial.Serial(com_port, 115200)

    def AT_komut_gonder(self, command_user):
        try:
            if (self.ser.isOpen() == False):
                self.ser.open()
        except AttributeError:
            print("Serial port could not be opened")
            #return
            quit() #burayı tekrar dusunelim, uygulamadan mı cikmali yoksa return ile fonksiyondan mı cikmali
        compose = ''
        compose = str(command_user) + "\r\n"
        self.ser.reset_input_buffer()
        self.ser.write(compose.encode())
        print("--------")
        #while()


        response = self.ser.read_all().decode()
        self.ser.read(5)
        while ( response == "\r\n"):
            pass

        print(response)

def sendATComm(command, desired_response, timeout=None):
    if timeout is None:
        timeout = timeout
    AT_komut_gonder(command)
    f_debug = False
    timer = millis()
    while 1:
        if (millis() - timer > timeout):  # BURADA HATA VAR NONE ATAMAYLA INTEGER KIYASLIYOR
            AT_komut_gonder(command)
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



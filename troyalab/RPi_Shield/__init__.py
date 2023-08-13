import time

try:
    import serial
except Exception as e:
    print("serial Library not found. Pls pip3 install serial")

try:
    import RPi.GPIO as GPIO
except Exception as e:
    print("RPi.GPIO Library not found.")

try:
    from decimal import *
except Exception as e:
    print("decimal Library not found.")
ser = serial.Serial()

#===========================================================================================================#
def millis():
    return int(time.time())

#===========================================================================================================#
class BG96:

    board          = ""    # shield name (BG96-RPi Shield)
    MQTT_BROKER_IP = ""    # MQTT IP Address
    MQTT_PORT      = 1883  # MQTT Port number #default 1883
    MQTT_CLIENT_ID = ""    # FOR MQTT
    MQTT_USER_NAME = ""    # port number
    MQTT_PASSWORD  = ""
    MQTT_TOPIC     = ""
    JSON_DATA      = "{\"fatih\":6.34,\"furkan\":51.51}"
    APN            = "internet"

    ip_address    = ""  # ip address for TCP or UDP
    port_number   = ""  # port number for TCP or UDP

    TB_MQTT_BROKER_IP = ""    # MQTT IP Address
    TB_MQTT_PORT      = 1883  # MQTT Port number #default 1883
    TB_MQTT_CLIENT_ID = ""    # FOR MQTT
    TB_MQTT_USER_NAME = ""    # port number
    TB_MQTT_PASSWORD  = ""
    TB_MQTT_TOPIC     = ""
    TB_JSON_DATA      = "{\"fatih\":6.34,\"furkan\":51.51}"

    timeout       = 3  # default timeout for function and methods on this library.
    MAX_ATTEMPT_TIME = 2
    ERROR         = -1

    BG96_POWERKEY = 23
    STATUS        = 10
    BG96_RESET    = 22

    # GSM Bands
    GSM_NO_CHANGE  = "0"
    GSM_900        = "1"  #Default #Türkiye(Turkey)
    GSM_1800       = "2"
    GSM_850        = "4"
    GSM_1900       = "8"
    GSM_ANY        = "F"  #default

    SCRAMBLE_ON    = "0"
    SCRAMBLE_OFF   = "1"

    # Cellular Modes
    AUTO_MODE      = 0
    GSM_MODE       = 1
    CATM1_MODE     = 2
    CATNB1_MODE    = 3

    # LTE Bands
    LTE_B1         = "1"
    LTE_B2         = "2"
    LTE_B3         = "4"
    LTE_B4         = "8"
    LTE_B5         = "10"
    LTE_B8         = "80"
    LTE_B12        = "800"
    LTE_B13        = "1000"
    LTE_B18        = "20000"
    LTE_B19        = "40000"
    LTE_B20        = "80000"
    LTE_B26        = "2000000"
    LTE_B28        = "8000000"
    LTE_B39        = "4000000000"  # catm1 only
    LTE_CATM1_ANY  = "400A0E189F" #default
    LTE_CATNB1_ANY = "A0E189F"   #default
    LTE_NO_CHANGE  = "0"

    # Special Characters
    CTRL_Z         = '\x1A'


#=========================================================================================
#                                 BG96 Config
#=========================================================================================
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
        time.sleep(0.2)
        GPIO.output(self.BG96_POWERKEY, 0)
        time.sleep(2)


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
            TIMEOUT = self.timeout
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

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Getting IMEI number
    """
    def getIMEI(self):
        return self.sendATComm("AT+CGSN", "OK\r\n")  # Identical command: AT+GSN

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Firmware info
    """
    def getFirmwareInfo(self):
        return self.sendATComm("AT+CGMR", "OK\r\n")  # Identical command: AT+GMR

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Hardware info
    """
    def getHardwareInfo(self):
        return self.sendATComm("AT+CGMM", "OK\r\n")  # Identical command: AT+GMM

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Returning Manufacturer Identification
    """
    def getManufacturerInfo(self):
        return self.sendATComm("AT+CGMI", "OK\r\n")  # Identical command: AT+GMI

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Setting GSM Band
    """
    def setGSMBand(self, gsm_band):
        self.compose = "AT+QCFG=\"band\","
        self.compose += str(gsm_band)
        self.compose += ","
        self.compose += str(self.LTE_NO_CHANGE)
        self.compose += ","
        self.compose += str(self.LTE_NO_CHANGE)

        self.sendATComm(self.compose, "OK\r\n")
        self.clear_compose()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Setting Cat.M1 Band
    """
    def setCATM1Band(self, catm1_band):
        self.compose = "AT+QCFG=\"band\","
        self.compose += str(self.GSM_NO_CHANGE)
        self.compose += ","
        self.compose += str(catm1_band)
        self.compose += ","
        self.compose += str(self.LTE_NO_CHANGE)

        self.sendATComm(self.compose, "OK\r\n")
        self.clear_compose()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Setting NB-IoT Band
    """
    def setNBIoTBand(self, nbiot_band):
        self.compose = "AT+QCFG=\"band\","
        self.compose += str(self.GSM_NO_CHANGE)
        self.compose += ","
        self.compose += str(self.LTE_NO_CHANGE)
        self.compose += ","
        self.compose += str(nbiot_band)

        self.sendATComm(self.compose, "OK\r\n")
        self.clear_compose()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get current band settings
    """
    def getBandConfiguration(self):
        return self.sendATComm("AT+QCFG=\"band\"", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Setting running mode.
    """
    def setMode(self, mode):
        if (mode == self.AUTO_MODE):
            self.sendATComm("AT+QCFG=\"nwscanseq\",00,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"nwscanmode\",0,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"iotopmode\",2,1", "OK\r\n")
            print("Modem configuration : AUTO_MODE")
            print("*Priority Table (Cat.M1 -> Cat.NB1 -> GSM)")
        elif (mode == self.GSM_MODE):
            self.sendATComm("AT+QCFG=\"nwscanseq\",01,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"nwscanmode\",1,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"iotopmode\",2,1", "OK\r\n")
            print("Modem configuration : GSM_MODE")
        elif (mode == self.CATM1_MODE):
            self.sendATComm("AT+QCFG=\"nwscanseq\",02,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"nwscanmode\",3,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"iotopmode\",0,1", "OK\r\n")
            print("Modem configuration : CATM1_MODE")
        elif (mode == self.CATNB1_MODE):
            self.sendATComm("AT+QCFG=\"nwscanseq\",03,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"nwscanmode\",3,1", "OK\r\n")
            self.sendATComm("AT+QCFG=\"iotopmode\",1,1", "OK\r\n")
            print("Modem configuration : CATNB1_MODE ( NB-IoT )")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get self.ip_address for TCP or UDP
    """
    def getIPAddress(self):
        return self.ip_address

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Set self.ip_address for TCP or UDP
    """
    def setIPAddress(self, ip):
        self.ip_address = ip

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get timout in ms
    """
    def getTimeout(self):
        return self.timeout

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Set timeout in ms
    """
    def setTimeout(self, new_timeout):
        self.timeout = new_timeout



#=============================================
#           SIM Related Functions
#=============================================

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # returns Mobile Subscriber Identity(IMSI)
    """
    def getIMSI(self):
        return self.sendATComm("AT+CIMI", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # returns Integrated Circuit Card Identifier(ICCID) number of the SIM
    """
    def getICCID(self):
        return self.sendATComm("AT+QCCID", "OK\r\n")


#=============================================
#          Network Service
#=============================================

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get signal quality
    """
    def getSignalQuality(self):
        return self.sendATComm("AT+CSQ", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get network information
    """
    def getQueryNetworkInfo(self):
        return self.sendATComm("AT+QNWINFO", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Connecting to base station of operator
    """
    def connectToOperator(self):
        print("Trying to connect base station of operator...")
        self.sendATComm("AT+CGATT=1", "")
        time.sleep(3)
        self.sendATComm("AT+CGATT?", "+CGATT: 1\r\n")
        self.getSignalQuality()

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get Network Registration Status
    """
    def getNetworkRegStatus(self):
        return self.sendATComm("AT+CREG?", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Set Network Registration Status
    """
    def setNetworkRegStatus(self):
        return self.sendATComm("AT+CREG=1", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Get Operator
    """
    def getOperator(self):
        return self.sendATComm("AT+COPS?", "OK\r\n")

    """
    # Date   : 06/08/2023
    # Author : Fatih Furkan
    # Set Operator APN
    """
    def setAPN(self, APN):
        print("Connect to Internet...")
        if APN is None:
            APN = self.APN
        self.compose = "AT+CGDCONT=1,\"IP\","
        self.compose += "\"" + APN +"\""
        self.sendATComm(self.compose, "OK")

        self.sendATComm("AT+CREG=1", "OK")
        self.sendATComm("AT+CREG?", "+CREG")
        self.sendATComm("AT+CEREG?", "+CEREG")
        self.sendATComm("AT+CGREG?", "+CGREG")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Get Operator APN
    """
    def getAPN_IPaddress(self):
        self.sendATComm("AT+CGPADDR", "+CGPADDR")


#=============================================
#          SMS Functions
#=============================================

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Sending SMS
    """
    def sendSMS(self, number, text):
        self.sendATComm("AT+CMGF=1", "OK\r\n")  # text mode
        time.sleep(0.5)

        self.compose = "AT+CMGS=\""
        self.compose += str(number)
        self.compose += "\""

        self.sendATComm(self.compose, ">")
        time.sleep(1)
        self.clear_compose()
        time.sleep(1)
        self.sendATCommOnce(text)
        self.sendATComm(self.CTRL_Z, "OK", 8)  # with 8 seconds timeout

#=============================================
#          GNSS Functions
#=============================================

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Turning on GNSS
    """
    def turnOnGNSS(self):
        self.sendATComm("AT+QGPS=1", "OK\r\n")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Turning off GNSS
    """
    def turnOffGNSS(self):
        self.sendATComm("AT+QGPSEND", "OK\r\n")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Getting latitude
    """
    def getLatitude(self):
        self.sendATComm("ATE0", "OK\r\n")
        self.sendATCommOnce("AT+QGPSLOC=2")
        timer = millis()
        while 1:
            self.response = ""
            while (ser.inWaiting()):
                self.response += ser.readline().decode('utf-8')
                if (self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1):
                    self.response = self.response.split(",")
                    ser.close()
                    return Decimal(self.response[1])
                if (self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1):
                    print(self.response)
                    ser.close()  #TODO burada serial port kapatiliyor
                    return 0

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Getting longitude
    """
    def getLongitude(self):
        self.sendATComm("ATE0", "OK\r\n")
        self.sendATCommOnce("AT+QGPSLOC=2")
        timer = millis()
        while 1:
            self.response = ""
            while (ser.inWaiting()):
                self.response += ser.readline().decode('utf-8')
                if (self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1):
                    self.response = self.response.split(",")
                    ser.close()
                    return Decimal(self.response[2])
                if (self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1):
                    print(self.response)
                    ser.close()  #TODO burada serial port kapatiliyor
                    return 0

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Getting speed in MPH
    """
    def getSpeedMph(self):
        self.sendATComm("ATE0", "OK\r\n")
        self.sendATCommOnce("AT+QGPSLOC=2")
        timer = millis()
        while 1:
            self.response = ""
            while (ser.inWaiting()):
                self.response += ser.readline().decode('utf-8')
                if (self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1):
                    self.response = self.response.split(",")
                    ser.close()
                    return round(Decimal(self.response[7]) / Decimal('1.609344'), 1)
                if (self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1):
                    print(self.response)
                    ser.close()  #TODO burada neden serial port kapatiliyor
                    return 0

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Getting speed in KPH
    """
    def getSpeedKph(self):
        self.sendATComm("ATE0", "OK\r\n")
        self.sendATCommOnce("AT+QGPSLOC=2")
        timer = millis()
        while 1:
            self.response = ""
            while (ser.inWaiting()):
                self.response += ser.readline().decode('utf-8')
                if (self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1):
                    self.response = self.response.split(",")
                    ser.close()
                    return Decimal(self.response[7])
                if (self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1):
                    print(self.response)
                    ser.close()  #TODO burada neden serial port kapatiliyor
                    return 0

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Getting fixed location
    """
    def getFixedLocation(self):
        return self.sendATComm("AT+QGPSLOC?", "+QGPSLOC:")


#=============================================
#      TCP & UDP Protocols Functions
#=============================================

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Configurating and activating TCP context
    """
    def activateContext(self):
        self.sendATComm("AT+QICSGP=1", "OK\r\n")
        time.sleep(1)
        self.sendATComm("AT+QIACT=1", "\r\n")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Deactivating TCP context
    """
    def deactivateContext(self):
        self.sendATComm("AT+QIDEACT=1", "\r\n")


    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Connecting to server via TCP
    """
    def connectToServerTCP(self):
        self.compose = "AT+QIOPEN=1,1"
        self.compose += ",\"TCP\",\""
        self.compose += str(self.ip_address)
        self.compose += "\","
        self.compose += str(self.port_number)
        self.compose += ",0,0"
        self.sendATComm(self.compose, "OK\r\n")
        self.clear_compose()
        self.sendATComm("AT+QISTATE=0,1", "OK\r\n")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Sending data via tcp.
    """
    def sendDataTCP(self, data):
        self.compose = "AT+QISEND=1,"
        self.compose += str(len(data))
        self.sendATComm(self.compose, ">")
        self.sendATComm(data, "SEND OK")
        self.clear_compose()

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Sending data HTTP
    """
    def sendDataHTTPConnect(self, server, token, data): # TODO bu fonksiyon daha sonra duzeltilecek
        self.compose = "AT+QHTTPCFG=\"contextid\",1"
        self.sendATComm(self.compose, "OK")
        self.clear_compose()
        self.compose = "AT+QHTTPCFG=\"requestheader\",1"
        self.sendATComm(self.compose, "OK")
        self.clear_compose()
        url = str("https://" + server + "/ ----- /")
        self.compose = "AT+QHTTPURL="
        self.compose += str(len(url))
        self.compose += ",80"
        self.setTimeout(20)
        self.sendATComm(self.compose, "CONNECT")
        self.clear_compose()
        self.sendDataComm(url, "OK")
        payload = "POST /----/ HTTP/1.1\r\nHost: " + server + "\r\nx-api-key: " + token + "\r\nContent-Type: application/json\r\nContent-Length: " + str(
            len(data)) + "\r\n\r\n"
        payload += data
        print("POSTED DATA")
        print(payload)
        print("----------------")
        self.compose = "AT+QHTTPPOST="
        self.compose += str(len(payload))
        self.compose += ",60,60"
        self.sendATComm(self.compose, "CONNECT")
        self.clear_compose()
        self.sendDataComm(payload, "OK")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Connecting to server via UDP
    """
    def startUDPService(self):
        port = "3005"
        self.compose = "AT+QIOPEN=1,1,\"UDP SERVICE\",\""
        self.compose += str(self.ip_address)
        self.compose += "\",0,"
        self.compose += str(port)
        self.compose += ",0"
        self.sendATComm(self.compose, "OK\r\n")
        self.clear_compose()
        self.sendATComm("AT+QISTATE=0,1", "\r\n")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Sending data via udp.
    """
    def sendDataUDP(self, data):
        self.compose = "AT+QISEND=1,"
        self.compose += str(len(data))
        self.compose += ",\""
        self.compose += str(self.ip_address)
        self.compose += "\","
        self.compose += str(self.port_number)
        self.sendATComm(self.compose, ">")
        self.clear_compose()
        self.sendATComm(data, "SEND OK")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Closing server connection
    """
    def closeConnection(self):
        self.sendATComm("AT+QICLOSE=1", "\r\n")


#=============================================
#                 INIT
#=============================================

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Init BG96 Module Basic
    """
    def InitiliazeTroyalabShield(self):
        self.setupGPIO()
        self.powerUp()
        self.sendATComm("ATE1", "OK\r\n")
        self.getIMEI()
        self.getFirmwareInfo()
        self.getHardwareInfo()
        self.connectToOperator()
        self.getSignalQuality()
        self.getQueryNetworkInfo()
        self.setNetworkRegStatus()


    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Connecting MQTT broker
    """
    def ConnectMQTTServer(self, MQTT_BROKER_IP = None, MQTT_PORT = None):
        if MQTT_BROKER_IP is None:
            MQTT_BROKER_IP = self.MQTT_BROKER_IP
        if MQTT_PORT is None:
            MQTT_PORT = self.MQTT_PORT

        self.compose = "AT+QMTOPEN=0,"
        self.compose += "\"" + MQTT_BROKER_IP + "\","
        self.compose += MQTT_PORT
        self.sendATComm(self.compose, "+QMTOPEN")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Configure MQTT Device
    """
    def MQTTDeviceConf(self, MQTT_CLIENT_ID = "Troyalab", MQTT_USER_NAME = "Troyalab"  , MQTT_PASSWORD = None):
        if MQTT_CLIENT_ID is None:
            MQTT_CLIENT_ID = self.MQTT_CLIENT_ID
        if MQTT_USER_NAME is None:
            MQTT_USER_NAME = self.MQTT_USER_NAME
        if MQTT_PASSWORD is None:
            MQTT_PASSWORD = self.MQTT_PASSWORD

        self.compose = "AT+QMTCONN=0,"
        self.compose += "\"" + MQTT_CLIENT_ID + "\","
        self.compose += "\"" + MQTT_USER_NAME + "\","
        self.compose += "\"" + MQTT_PASSWORD + "\""
        self.sendATComm(self.compose, "+QMTCONN")

    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Publish data MQTT
    """
    def publishDataMQTT(self, MQTT_TOPIC = "v1/devices/me/telemetry" ,JSON_DATA="{\"fatih\":6.34,\"furkan\":51.51}"):
        if MQTT_TOPIC is None:
            MQTT_TOPIC = self.MQTT_TOPIC
        if JSON_DATA is None:
            JSON_DATA = self.JSON_DATA
        self.compose = "AT+QMTPUB=0,0,0,0,"
        self.compose += "\"" + MQTT_TOPIC + "\""
        self.sendATComm(self.compose, ">" ,10)

        self.compose = JSON_DATA
        self.sendATComm(self.compose,"{")
        command_variable = chr(26)
        ser.write(command_variable.encode('utf-8'))
        time.sleep(2)


    """
    # Date   : 11/08/2023
    # Author : Fatih Furkan
    # Basic configure Thignsboard MQTT broker
    """
    def ThingboardMQTTBasicConfig(self,MQTT_BROKER_IP = None, MQTT_PORT = None, MQTT_CLIENT_ID = None, MQTT_USER_NAME =None  , MQTT_PASSWORD = None ): # TODO bu fonksiyon daha sonra duzeltilecek

        if MQTT_BROKER_IP is None or MQTT_PORT is None:
            print("Broker veya port yanlis")
        else:
            self.TB_MQTT_BROKER_IP = MQTT_BROKER_IP
            self.TB_MQTT_PORT = MQTT_PORT
            self.ConnectMQTTServer(MQTT_BROKER_IP, MQTT_PORT)
        time.sleep(1)
        if MQTT_CLIENT_ID is None or MQTT_USER_NAME is None or MQTT_PASSWORD is None:
            print("MQTT_CLIENT_ID,  MQTT_USER_NAME veya MQTT_PASSWORD yanlis")
        else:
            self.TB_MQTT_CLIENT_ID = MQTT_CLIENT_ID
            self.TB_MQTT_USER_NAME = MQTT_USER_NAME
            self.TB_MQTT_PASSWORD = MQTT_PASSWORD
            self.MQTTDeviceConf(MQTT_CLIENT_ID,MQTT_USER_NAME,MQTT_PASSWORD)

    """
    # Date   : 10/08/2023
    # Author : Fatih Furkan
    # TB'a veriyi mqtt token formatinda gonderir
    """
    def ThingboardMQTT_TokenConfig(self,MQTT_BROKER_IP = None, MQTT_PORT = None,  MQTT_USER_NAME =None  , MQTT_PASSWORD = None ): # TODO bu fonksiyon daha sonra duzeltilecek

        if MQTT_BROKER_IP is None or MQTT_PORT is None:
            print("Broker veya port yanlis")
        else:
            self.TB_MQTT_BROKER_IP = MQTT_BROKER_IP
            self.TB_MQTT_PORT = MQTT_PORT
            self.ConnectMQTTServer(MQTT_BROKER_IP, MQTT_PORT)
        time.sleep(1)
        if MQTT_USER_NAME is None or MQTT_PASSWORD is None:
            print("MQTT_CLIENT_ID,  MQTT_USER_NAME veya MQTT_PASSWORD yanlis")
        else:
            self.TB_MQTT_USER_NAME = MQTT_USER_NAME
            self.TB_MQTT_PASSWORD = MQTT_PASSWORD
            self.MQTTDeviceConf(MQTT_USER_NAME,MQTT_PASSWORD)





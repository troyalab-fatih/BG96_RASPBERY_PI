import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
import os
import time
import sys
import datetime
import subprocess
import paho.mqtt.client as mqtt
import json





GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)    # Use physical pin numbering
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

MQTT_HOST_NAME = "194.31.59.188"
Token_sensor   = "SENSOR_DATA"
########################################################
# Main
########################################################
get_ip_add = subprocess.Popen(
    "hostname -I", shell=True, stdout=subprocess.PIPE).stdout
ip_add = get_ip_add.read()

date_ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
timer_post_start = time.time()


sensor_data = {'temperature': 0, 'humidity': 0}

client = mqtt.Client()
client.loop_start()

# -----------------------------------------------------
# Fonskiyonlar
# -----------------------------------------------------
def sensor_den_veri_oku():
  try:
      #temp = SHT21.read_temperature()
      temp = 29.4  #ornek
      time.sleep(1)
      #hum = SHT21.read_humidity()
      sensor_data = {'temperature': 0, 'humdity': 0, 'dtime': 0}
      try:
          client = mqtt.Client()
          client.username_pw_set(Token_sensor)
          client.connect(MQTT_HOST_NAME, 1883, 60)
          client.loop_start()
          sensor_data['temperature'] = temp  #ornek
          sensor_data['humdity'] = 65        #ornek
          sensor_data['dtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
          print('\n%.9s' % datetime.datetime.now().strftime("%H:%M:%S"))
          time.sleep(3)
          print(' T:%.1f C \n' % temp)
          time.sleep(3)
          print(Token_sensor)
          time.sleep(3)
          client.loop_stop()
          client.disconnect()
      except:
        print("MQTT Hata")
  except:
    print("SHT Disable")
    pass



while True: # Run forever

  GPIO.output(4, GPIO.HIGH) # Turn on
  sleep(1)                  # Sleep for 1 second
  GPIO.output(4, GPIO.LOW)  # Turn off
  sleep(1)                  # Sleep for 1 second
  sensor_den_veri_oku()

  sleep(2)  # Sleep for 1 second
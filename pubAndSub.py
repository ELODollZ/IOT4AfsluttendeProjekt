# The MIT License (MIT)
# Copyright (c) 2019 Mike Teachman
# https://opensource.org/licenses/MIT
#
# Example MicroPython and CircuitPython code showing how to use the MQTT protocol with Adafruit IO, to  
# publish and subscribe on the same device
#
# Tested using the releases:
#   ESP8266
#       MicroPython 1.9.3
#       MicroPython 1.9.4
#       MicroPython 1.10
#       CircuitPython 2.3.1     (needs addition of CircuitPython specific umqtt module)
#       CircuitPython 3.0.0     (needs addition of CircuitPython specific umqtt module)
#   ESP32
#       MicroPython 1.9.4       (needs addition of MicroPython umqtt module)
#       MicroPython 1.10
#
# Tested using the following boards:
#   Adafruit Feather HUZZAH ESP8266
#   Adafruit Feather HUZZAH ESP32
#   WeMos D1 Mini
#
# User configuration parameters are indicated with "ENTER_".  

import network
import time
from umqtt.robust2 import MQTTClient
import os
import gc
import sys
from credentials import credentials 
# the following function is the callback which is 
# called when subscribed data is received
def cb(topic, msg):
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))

# WiFi connection information
#WIFI_SSID = credentials['ssid']
#WIFI_PASSWORD = credentials['password']

# turn off the WiFi Access Point
#ap_if = network.WLAN(network.AP_IF)
#ap_if.active(False)

# connect the device to the WiFi network
#wifi = network.WLAN(network.STA_IF)
#wifi.active(True)
#wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
#MAX_ATTEMPTS = 20
#attempt_count = 0
#while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
#    attempt_count += 1
#    time.sleep(1)

#if attempt_count == MAX_ATTEMPTS:
#    print('could not connect to the WiFi network')
#    sys.exit()

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
ADAFRUIT_IO_URL = credentials['ADAFRUIT_IO_URL']
ADAFRUIT_USERNAME = credentials['ADAFRUIT_USERNAME']
ADAFRUIT_IO_KEY = credentials['ADAFRUIT_IO_KEY']
ADAFRUIT_IO_FEEDNAME = credentials['ADAFRUIT_IO_FEEDNAME']

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# publish free heap statistics to Adafruit IO using MQTT
# subscribe to the same feed
#
# format of feed name:  
#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
mqtt_feedname1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, "iot4.toggle-button"), 'utf-8')
client.set_callback(cb)      
client.subscribe(mqtt_feedname1)  
PUBLISH_PERIOD_IN_SEC = 10 
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
accum_time = 0

def PublishMSG(Test):
        client.publish(mqtt_feedname,    
                        bytes(str(Test), 'utf-8'), 
                        qos=0)
def SubScribeMSG():
    #client.set_callback(cb)
    client.subscribe(mqtt_feedname)
    print("FeedLiveLog")
    client.subscribe(mqtt_feedname1)
    print("FeedButton")
    MSG = client.check_msg()
    print(MSG)

PublishMSG("Test Func")
SubScribeMSG()

client.disconnect()
print("ending")
sys.exit()
#while True:
#    try:
#        # Publish
#        if accum_time >= PUBLISH_PERIOD_IN_SEC:
#            #free_heap_in_bytes = gc.mem_free()
#            free_heap_in_bytes = "Testing Changes"
#            print('Publish:  feed = {}'.format(free_heap_in_bytes))
# 
#            accum_time = 0                
#        
#        # Subscribe.  Non-blocking check for a new message.  
#        
#
#        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
#        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
#    except KeyboardInterrupt:
#        print('Ctrl-C pressed...exiting')
#        client.disconnect()
#        sys.exit()
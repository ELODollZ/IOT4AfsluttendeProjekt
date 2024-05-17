#!/usr/bin/env python3
# Author: NyboMønster
# Sources: 
# https://github.com/aloishockenschlohe/dpm86_power_supply

#Imports
import _thread as Thread
from time import sleep
from UART2Protocol import UART2Thread
from SimpleProtocol import SimpleThread
from machine import Pin, UART
from credentials import credentials 
from umqtt.robust import MQTTClient
import os
import network
import sys
from credentials import credentials
### AdaFruit Sourced ###
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(credentials['ssid'], credentials['password'])

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()
# print("Everything connected") 

uart2 = UART(2, baudrate=9600, tx=17, rx=16)
ControllerPin = Pin(4)
ProtocolToUse = credentials["ProtocolToUse"]
GlobalMSG = []
# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
#Connects to MQTT Adafruit
def cb(topic, msg):
    global GlobalMSG
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    msg = msg.decode('utf-8')
    #print(msg)
    GlobalMSG.append(msg)
    
client = MQTTClient(client_id=mqtt_client_id, 
                    server=credentials['ADAFRUIT_IO_URL'], 
                    user=credentials['ADAFRUIT_USERNAME'], 
                    password=credentials['ADAFRUIT_IO_KEY'],
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()
topic = ""
msg = ""
# MQTT Feeds for AdaFruit
mqtt_MainFeed = bytes('{:s}/feeds/{:s}'.format(credentials['ADAFRUIT_USERNAME'], credentials['ADAFRUIT_IO_FEEDNAME']), 'utf-8')
mqtt_ToggleButton = bytes('{:s}/feeds/{:s}'.format(credentials['ADAFRUIT_USERNAME'], "iot4.toggle-button"), 'utf-8')


def PublishMSG(MSGToPub):
        client.publish(mqtt_MainFeed,    
                        bytes(str(MSGToPub), 'utf-8'), 
                        qos=0)
def SubScribeMSG():
    client.set_callback(cb)
    client.subscribe(mqtt_MainFeed)
    client.subscribe(mqtt_ToggleButton)
    client.check_msg()
    print(GlobalMSG)
    
    
 
#Main
MSG = "Test"
Test = False
if Test == True:
    try:
        if ProtocolToUse == "UART2":
            Thread.start_new_thread(PowerCTLSwitchThread,(ControllerPin, uart2))
        elif ProtocolToUse == "Simple":
            Thread.start_new_thread(SimpleThread,(ControllerPin, uart2))
    except Exception as e:
        print(f"Exception because error in starting thread: {e}")

while True:
    try:
        PublishMSG("Test Func")
        SubScribeMSG()
        if '0' in GlobalMSG and '1' in GlobalMSG:
            print("Button Pressed")
            #ControllerPin.on()
        else:
            print("No button")
        GlobalMSG.clear()
        print("-----		-----")
        sleep(1)
    except OSError as e:
        print(f"OSError in: {e}")
        mqtt.c.disconnect()
        mqtt.sys.exit()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
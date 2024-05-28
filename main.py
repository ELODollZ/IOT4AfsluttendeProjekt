#!/usr/bin/env python3
# Author: NyboMønster
# Sources: 
# https://github.com/aloishockenschlohe/dpm86_power_supply		#pubAndSub.py

#Imports
from machine import Pin, UART
from time import sleep
import os
import network
import sys
from umqtt.robust2 import MQTTClient
from credentials import credentials 

from ModBusRTUController import SetVoltageAndCurrentOnDPM8624, SetCurrentOnDPM8624, SetVoltageOnDPM8624, RequestDPM8624Setting


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
print("Everything connected") 

uart2 =  credentials["ProtocolToUse"]
TransmiteNOWPin = Pin(credentials['TransmitPin'])
GlobalMSG = []
# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
#Connects to MQTT Adafruit
def cb(topic, msg):
    global GlobalMSG
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    msg = msg.decode('utf-8')
    print(msg)
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
mqtt_ToggleButton = bytes('{:s}/feeds/{:s}'.format(credentials['ADAFRUIT_USERNAME'], credentials['ADAFRUIT_TOGGLE_BUTTON']), 'utf-8')
mqtt_Kontroller = bytes('{:s}/feeds/{:s}'.format(credentials['ADAFRUIT_USERNAME'], credentials['ADAFRUIT_KONTROLLER']), 'utf-8')

def PublishMSG(MSGToPub):
        client.publish(mqtt_MainFeed,    
                        bytes(str(MSGToPub), 'utf-8'), 
                        qos=0)
def SubScribeMSG():
    client.set_callback(cb)
    client.subscribe(mqtt_MainFeed)
    client.subscribe(mqtt_ToggleButton)
    client.subscribe(mqtt_Kontroller)
    client.check_msg()
    print(GlobalMSG)
    
#Main  
DPM8624Address = 3

while True:
    try:
        RequestDPM8624Setting(uart2, TransmiteNOWPin, DPM8624Address)
        SubScribeMSG()
        if '0' in GlobalMSG or '1' in GlobalMSG:
            MSG = "Button Pressed"
            SetVoltageAndCurrentOnDPM8624(uart2, TransmiteNOWPin, DPM8624Address, 42, 2)
            PublishMSG(MSG)
        else:
            print("No button toggled")
        if '2' in GlobalMSG or '3' in GlobalMSG:
            MSG = "Charge now"
            SetVoltageOnDPM8624(uart2, TransmiteNOWPin, DPM8624Address, 36)
            SetCurrentOnDPM8624(uart2, TransmiteNOWPin, DPM8624Address, 1.5)
            PublishMSG(MSG)
        else:
            print("No button pressed")
        if 'SolarPowerOn, turning on' in GlobalMSG :
            print("Solar Power detected, Turning on")
        elif 'SolarPowerOff' in GlobalMSG:
            print("No Solar Power, Turning off")
        GlobalMSG.clear()
        print("-----		-----")
        sleep(1)
    except OSError as e:
        print(f"OSError in: {e}")
        client.disconnect()
        sys.exit()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
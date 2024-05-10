#!/usr/bin/env python3
# Author: NyboMønster

#Imports
from machine import Pin
import _thread as Thread
from time import sleep
import umqtt_robust2 as mqtt

#Code to control power-switching
def PowerCTLSwitchThread(PowerSwitch):
    try:
        while True:
            sleep(1)
            print("Test PowerSwitch ThreadLoop")
    except Exception as e:
        print(f"Exception with: {e}")

def MSGBrokerToAdaFruitThread(MSG):
    try:
        mqtt.web_Print(MSG)
        #print("Test MSG ThreadLoop")
        sleep(0.5)
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.syncWithAdafruitIO() # igangsæt at sende og modtage data med Adafruit IO      
    except Exception as e:
        print(f"Exception with: {e}")
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()
 

#Main
PowerSwitch = "True"
MSG = "Test"
#try:
#    Thread.start_new_thread(PowerCTLSwitchThread,(PowerSwitch))
#    Thread.start_new_thread(MSGBrokerToAdaFruitThread,(MSG))
#except Exception as e:
#    print(f"Exception because error in starting thread: {e}")

while True:
    try:
        print("Testing")
        sleep(1)
        PowerCTLSwitchThread(PowerSwitch)
        MSGBrokerToAdaFruitThread(MSG)
    except Exception as e:
        pass
    except OSError as e:
        print(f"OSError in: {e}")
        mqtt.c.disconnect()
        mqtt.sys.exit()
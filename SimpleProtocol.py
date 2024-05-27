#!/usr/bin/env python3
# Author: NyboMønster

from machine import Pin, UART
from time import sleep

def SimpleThread(PowerSwitch, uart2):
    try:
        print("Sending command")
        PowerSwitch.on()
        uart2.write(':01w10=2400,/r/n,')
        PowerSwitch.off()
        MSG = uart2.read()
        print("Got From:", MSG)
        sleep(1)
        PowerSwitch.on()
        print("Sending command")
        uart2.write(':01w11=0200,\r\n')
        print("Sending command")
        uart2.write(':01w12=0')
        sleep(2)
        print("Sending command")
        uart2.write('01w20=10,10,')
        PowerSwitch.off()
        print("Modtager information")
        MSG = uart2.read()
        print("Got From:", MSG)
        sleep(2)
        PowerSwitch.on()
        uart2.write(':01r00=0,')
        MSG = uart2.read()
        print(MSG)
        sleep(2)
        PowerSwitch.off()
    except Exception as e:
        print(f"Exception because error in starting thread: {e}")
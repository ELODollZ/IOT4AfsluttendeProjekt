#!/usr/bin/env python3
# Author: NyboMønster

from machine import Pin, UART
from time import sleep

def SimpleThread(PowerSwitch, uart2):
    try:
        while True:
            print("Test SimpleProtocol Thread")
            uart2.write(':01w10=2400,/r/n,')
            sleep(1)
            MSG = uart2.read(20)
            print(MSG)
            sleep(2)
            uart2.write(':01w11=0200,\r\n')
            sleep(2)
            uart2.write(':01w12=0')
            sleep(2)
            uart2.write('01w20=10,10,')
            MSG = uart2.read()
            print(MSG)
            sleep(2)
            uart2.write(':01r00=0,')
            MSG = uart2.read(20)
            print(MSG)
            sleep(2)
    except Exception as e:
        print(f"Exception with: {e}")
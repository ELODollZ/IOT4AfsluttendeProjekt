#!/usr/bin/env python3
# Author: NyboMønster

from machine import Pin, UART

def UART2Thread(PowerSwitch, uart2):
    try:
        while True:
            print("Test PowerSwitch ThreadLoop")
            uart2.write('output')
            sleep(1)
            MSG = uart2.read()
            print(MSG)
            sleep(2)
            uart2.write('output 1')
            sleep(2)
            uart2.write('o off')
            sleep(2)
            uart2.write('a')
            MSG = uart2.read()
            print(MSG)
            sleep(2)
            uart2.write('v')
            MSG = uart2.read()
            print(MSG)
            sleep(2)
    except Exception as e:
        print(f"Exception with: {e}")
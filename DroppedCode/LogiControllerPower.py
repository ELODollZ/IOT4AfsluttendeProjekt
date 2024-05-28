#!/usr/bin/env python3
# Author: NyboMønster

#Imports
from machine import Pin
from credentials import credentials
from ModBusRTUController import TransmitNow
#Pin's on ESP32
M1 = Pin(credentials['Pin_For_Mosfets1'])
M2 = Pin(credentials['Pin_For_Mosfets2'])
M3 = Pin(credentials['Pin_For_Mosfets3'])

#Main code
def SolONBatOFFPSUOn(M1, M2, M3):
    M1.On()
    M2.Off()
    M3.Off()
    TransmitNow(True)
    print("Solurpanel making power for us :D")

def SolOffBatOnPSUOn(M1, M2, M3):
    M1.Off()
    M2.On()
    M3.On()
    TransmitNow(False)
    print("batteri making power for us :D")

def SolOnBatOffPSUOff(M1, M2, M3):
    M1.Off()
    M2.On()
    M3.Off()
    TransmitNow(True)
    print("Charging batteri for later use :D")

def WhereToPower(SolOn, BatOn, PSUOn):
    if SolOn == True and BatOn == False and PSUOn == False :
         SolONBatOFFPSUOn(M1, M2, M3)
    elif SolOn == False and BatOn == True and PSUOn == True:
        SolOffBatOnPSUOn(M1, M2, M3)
    elif SolOn == False and BatOn == False and PSUOn == True:
        SolOnBatOffPSUOff(M1, M2, M3)
    else:
        print("Wrong Arugments for deciding where to power :(")
#!/usr/bin/env python3
# Author: NyboMønster

#Imports
from machine import Pin
from credentials import credentials
#Pin's on ESP32
M1 = Pin(credentials['Pin_For_Mosfets1'])
M2 = Pin(credentials['Pin_For_Mosfets2'])
M3 = Pin(credentials['Pin_For_Mosfets3'])

#Main code
def SolONBatOFFPSUOn(M1, M2, M3):
    M1.On()
    M2.Off()
    M3.Off()
    print("Solurpanel making power for us :D")

def SolOffBatOnPSUOn(M1, M2, M3):
    M1.Off()
    M2.On()
    M3.On()
    print("batteri making power for us :D")

def SolOnBatOffPSUOff(M1, M2, M3):
    M1.Off()
    M2.On()
    M3.Off()
    print("Charging batteri for later use :D")

def WhereToPower(SolOn, BatOn, PSUOn):
    if SolOn == True and PSUOn == False:
         SolONBatOFFPSUOn(M1, M2, M3)
    elif BatOn == True and PSUOn == True:
        SolONBatOFFPSUOn(M1, M2, M3)
    elif SolOn == True and PSUOn == True:
        SolOnBatOffPSUOff(M1, M2, M3)
    else:
        print("Wrong Arugments for deciding where to power :(")
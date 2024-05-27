from machine import Pin, UART
from time import sleep

uart2 = UART(2, baudrate=9600, tx=17, rx=16)
MosfetPinControl1 = Pin(0)
MosfetPinControl2 = Pin(2)
MosfetPinControl3 = Pin(15)
TransmiteNOWPin = Pin(2,Pin.OUT)
RecieveNOWPin = Pin(4,Pin.OUT)
TransmiteNOWPin.value(0)
RecieveNOWPin.value(0)

while True:
    TransmiteNOWPin.value(1)
    RecieveNOWPin.value(1)
    sleep(0.15)
    uart2.write(':01w10=2400, /r/n,')
    TransmiteNOWPin.value(0)
    RecieveNOWPin.value(0)
    sleep(0.15)
    MSG = uart2.read()
    RecieveNOWPin.value(1)
    TransmiteNOWPin.value(0)
    print(MSG)
    sleep(1)
    #print("attempted to set voltage and amp")
#!/usr/bin/env python3
# Author: NyboMønster
# Sources: 
# https://docs.python.org/3/library/struct.html
from machine import Pin, UART
from time import sleep
import struct
from credentials import credentials

DataEnableReceiveDisabled = Pin(credentials['TransmitPin'], Pin.OUT)
uart2 = UART(2, baudrate=9600, tx=credentials['TX'], rx=credentials['RX'], bits=8, parity=None, stop=1)

def TransmitNow(DataEnableReceiveDisabled, enable):
    DataEnableReceiveDisabled.value(1 if enable else 0)
TransmitNow(DataEnableReceiveDisabled, False)

def CRC16Bites(data: bytes )-> int:
    CRC = 0xFFFF
    for Byte in data:
        CRC ^= Byte
        for Bite in range(8):
            if (CRC & 1) != 0:
                CRC >>= 1
                CRC ^= 0xA001
            else:
                CRC >>= 1
    return CRC

def CheckResponse(Response):
    print("Response: ", Response)
    if len(Response) < 5:
        ResponseMSG = 'Ugyldigt svar'
        print(ResponseMSG)
        return ResponseMSG
    ReceivedCRC = struct.unpack('<H', Response[-2:])[0]
    CalculatedCRC = CRC16Bites(Response[:-2])
    print("Received CRC: ", ReceivedCRC, "Calculated CRC: ", CalculatedCRC)
    if ReceivedCRC != CalculatedCRC:
        ResponseMSG = 'Ugyldigt CRC svar'
        print(ResponseMSG)
        return ResponseMSG
    Address, FunktionCode, ByteCount = struct.unpack('>BBB', Response[:3])
    if FunktionCode & 0x80:
        errorCode = struct.unpack('>B', Response[3:4])[0]
        print(f"ErrorCode: {errorCode}")
        return errorCode
    DataFromDPM8624 = struct.unpack(f'>{ByteCount//2}H', Response[3:3+ByteCount])
    print("DataFromDPM: ", DataFromDPM8624)
    return DataFromDPM8624

def RequestDPM8624Setting(uart2, DataEnableReceiveDisabled, Address):
    Request = struct.pack('>BBHH', Address, 3, 0x0000, 2)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    MSG = 'Request sent:', ''.join(['{:02x}'.format(x) for x in Request])
    print(MSG)
    sleep(0.01)
    TransmitNow(DataEnableReceiveDisabled, False)
    sleep(2)
    Response = uart2.read()
    print("Rå Data: ", Response)
    if Response:
        DataFromDPM8624 = CheckResponse(Response)
        if isinstance(DataFromDPM8624, list):
            ResponseMSG = 'Answar Received:', ''.join(['{:02x}'.format(x) for x in DataFromDPM8624])
            print(ResponseMSG)
            return ResponseMSG
    else:
        ResponseMSG = 'Ingen svar modtaget'
        print(ResponseMSG)
        return ResponseMSG

def SetVoltageOnDPM8624(uart2, DataEnableReceiveDisabled, Address, Voltage):
    FunctionCode = 6
    RegisterAddress = 0x0000
    Value = int(Voltage * 100)
    Request = struct.pack('>BBHH', Address, FunctionCode, RegisterAddress, Value)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    RequestMSG = 'Setting Voltage;', Voltage, 'Volt, Request Sent:', ''.join(['{:02x}'.format(x) for x in Request])
    print(RequestMSG)
    sleep(0.01)
    TransmitNow(DataEnableReceiveDisabled, False)
    sleep(2)
    Response = uart2.read()
    if Response:
        ResponseMSG = 'Svar modtaget:', ''.join(['{:02x}'.format(x) for x in Response])
        print(ResponseMSG)
        return ResponseMSG
    else:
        ResponseMSG = 'Ingen svar modtaget'
        print(ResponseMSG)
        return ResponseMSG
    
def SetCurrentOnDPM8624(uart2, DataEnableReceiveDisabled, Address, Current):
    FunctionCode = 6
    RegisterAddress = 0x0001
    Value = int(Current * 1000)
    Request = struct.pack('>BBHH', Address, FunctionCode, RegisterAddress, Value)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    RequestMSG = 'Setting Current;', Current, 'Amp, Request sent:', ''.join(['{:02x}'.format(x) for x in Request])
    print(RequestMSG)
    sleep(0.01)
    TransmitNow(DataEnableReceiveDisabled, False)
    sleep(2)
    Response = uart2.read()
    if Response:
        ResponseMSG = 'Svar modtaget:', ''.join(['{:02x}'.format(x) for x in Response])
        print(ResponseMSG)
        return ResponseMSG
    else:
        ResponseMSG = 'Ingen svar modtaget'
        print(ResponseMSG)
        return ResponseMSG

def SetVoltageAndCurrentOnDPM8624(uart2, DataEnableReceiveDisabled, Address, Voltage, Current):
    FunctionCode = 16
    RegisterAddress = 0x0000
    Values = [int(Voltage * 100), int(Current * 1000)]
    AntalForsendelser = len(Values)
    ByteAntal = AntalForsendelser * 2
    Request = struct.pack('>BBHHB', Address, FunctionCode, RegisterAddress, AntalForsendelser, ByteAntal)
    for value in Values:
        Request += struct.pack('>H', value)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    RequestMSG = 'Setting Voltage;', Voltage, 'Volt,', 'Setting Current;', Current, 'Amp,',' Request sent:', ''.join(['{:02x}'.format(x) for x in Request])
    print(RequestMSG)
    sleep(0.01)
    TransmitNow(DataEnableReceiveDisabled, False)
    sleep(2)
    Response = uart2.read()
    if Response:
        ResponseMSG = 'Svar modtaget:', ''.join(['{:02x}'.format(x) for x in Response])
        print(ResponseMSG)
        return ResponseMSG
    else:
        ResponseMSG = 'Ingen svar modtaget'
        print(ResponseMSG)
        return ResponseMSG

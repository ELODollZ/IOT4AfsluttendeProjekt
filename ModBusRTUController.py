from machine import Pin, UART
from time import sleep
import struct
from credentials import credentials

DataEnableReceiveDisabled = Pin(credentials['TransmitPin'], Pin.OUT)
uart2 =  credentials["uart2"]

def TransmitNow(DataEnableReceiveDisabled, enable):
    DataEnableReceiveDisabled.value(1 if enable else 0)

def CRC16Bites(data: bytes )-> int:
    CRC = 0xFFFF
    for Position in data:
        CRC ^= Position
        for Bite in range(8):
            if (CRC & 1) != 0:
                CRC >>= 1
                CRC ^= 0xA001
            else:
                CRC >> 0
    return CRC

def CheckResponse(Response):
    if len(Response) < 5:
        ResponseMSG = 'Ugyldigt svar'
        print(ResponseMSG)
        return ResponseMSG
    ReceivedCRC = struct.unpack('<H', Response[-2:])[0]
    CalculatedCRC = CRC16Bites(Response[:-2])
    if ReceivedCRC != CalculatedCRC:
        ResponseMSG = 'Ugyldigt svar'
        print(ResponseMSG)
        return ResponseMSG
    Address, FunktionCode, ByteCount = struct.unpack('>BBB', Response[:3])
    if FunktionCode & 0x80:
        errorCode = struct.unpack('>B', Response[3:4])[0]
        print(f"ErrorCode: {errorCode}")
        return errorCode
    DataFromDPM8624 = struct.unpack(f'>{ByteCount//2}H', Response[3:-2])
    return DataFromDPM8624

def RequestDPM8624Setting(uart2, DataEnableReceiveDisabled, Address):
    Request = struct.pack('>BBHH', Address, 3, 0x0000, 2)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    MSG = 'Forspørgelsen sendt:', ''.join(['{:02x}'.format(x) for x in Request])
    print(MSG)
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

def SetVoltageOnDPM8624(uart2, DataEnableReceiveDisabled, Address, Voltage):
    FunctionCode = 6
    RegisterAddress = 0x0000
    Value = int(Voltage * 100)
    Request = struct.pack('>BBHH', Address, FunctionCode, RegisterAddress, Value)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    RequestMSG = 'Sætter spænding;', Voltage, 'Volt, Forespørgsel sendt:', ''.join(['{:02x}'.format(x) for x in Request])
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
    RegisterAddress = 0x0000
    Value = int(Current * 1000)
    Request = struct.pack('>BBHH', Address, FunctionCode, RegisterAddress, Value)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    RequestMSG = 'Sætter strøm;', Current, 'Amp, Forespørgsel sendt:', ''.join(['{:02x}'.format(x) for x in Request])
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
    Value = [int(Voltage*100), int(Current * 1000)]
    AntalForsendelser = len(Value)
    ByteAntal = AntalForsendelser * 2
    Request = struct.pack('>BBHH', Address, FunctionCode, RegisterAddress, AntalForsendelser, ByteAntal)
    for value in Value:
        Request += struct.pack('<H', value)
    CRC = CRC16Bites(Request)
    Request += struct.pack('<H', CRC)
    TransmitNow(DataEnableReceiveDisabled, True)
    uart2.write(Request)
    RequestMSG = 'Sætter spænding;', Voltage, 'Volt,', 'Sætter Strøm;', Current, 'Amp,',' Forespørgsel sendt:', ''.join(['{:02x}'.format(x) for x in Request])
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
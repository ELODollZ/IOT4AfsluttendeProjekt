from machine import Pin, UART
from time import sleep
import struct

uart = UART(2, baudrate=9600, bits= 8, parity=None, stop=1, tx=17, rx=16)
RePin = Pin(2, Pin.OUT)
DePin = Pin(4, Pin.OUT)

def enable_transmitter(enable):
    DePin(1 if enable else 0)
    RePin(1 if enable else 0)
    print('Transmitter Enabled' if enable else 'Receiver Enabled')


def crc16(data: byte) -> int:
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

def send_modbus_request(slave_addr, function_Code, start_addr, quantity):
    request = struct.pack('>BBHH', slave_addr, function_code, start_addr, quantity)
    crc = crc16(request)
    request += struct.pack('<H', crc)
    
    enable_transmitter(True)
    
    uart.write(request)
    print('Forespørgsel sendt:', request)
    sleep(0.1)
    
    enable_transmitter(False)
    
    sleep(1)
    response = uart.read()
    print('Svar rå data:', response)
    if response:
        print('Svar modtaget:', response)
        return response
    else:
        print('ingen svar modtaget')
        return None

def parse_response(response):
    if len(response) < 5:
        print("Ugyldigt svar")
        return None
    received_crc = struct.unpack('<H', response[-2:])[0]
    calculated_crc = crc16(response[-2:])
    if received_crc != calculated_crc:
        print("CRC fejl")
        return None
    
    slave_addr, function_code, byte_count = struct.unpack('>BBB', response[:3])
    if function_code & 0x80:
        error_code = struct.unpack('>B', response[3:4])[0]
        print(f"Fejlkode: {error_code}")
        return None
    data = struct.unpack(f'>{byte_count//2}H', response[3:-2])

    
slave_addr = 1
function_code = 3
start_addr = 0x0000
quantity = 2
while True:
    sleep(2)
    response = send_modbus_request(slave_addr, function_code, start_addr, quantity)
    if response:
        data = parse_response(response)
        if data:
            print("Spændingsindstilling (V):", data[0])
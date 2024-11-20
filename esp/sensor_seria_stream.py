import asyncio as asyncio
import network
import json
from lib.ws import AsyncWebsocketClient, OP_PONG
import struct

from machine import I2C, Timer, Pin
import math
import struct
from lib.mpu9250 import MPU9250
from lib.mpu6500 import MPU6500, ACCEL_FS_SEL_8G, GYRO_FS_SEL_1000DPS
import time
import socket




i2c = I2C(1, sda=21, scl=22, freq=400000)
print(i2c.scan())

sensor6500 = MPU6500(i2c, accel_fs=ACCEL_FS_SEL_8G, gyro_fs=GYRO_FS_SEL_1000DPS)
sensor = MPU9250(i2c, mpu6500=sensor6500)

sensor.mpu6500._register_char(0x1A, 0x07) #Dectivate lpf gyro
sensor.mpu6500._register_char(0x1D, 0x08) #Deactivate lpf acc

sensor.mpu6500._register_char(0x38, 0x01) #Activate DR interrupt
current_int_pin_cfg = sensor.mpu6500._register_char(0x37) 
current_int_pin_cfg &= 0b11001111 # Clear bits 5 and 4
current_int_pin_cfg |= 0b00110000 # Set desired bits
sensor.mpu6500._register_char(0x37, current_int_pin_cfg)


new_data = asyncio.Event()
def new_data_callback(pin):
    new_data.set()

interrupt_pin = Pin(36, Pin.IN, pull=None)
interrupt_pin.irq(trigger=Pin.IRQ_RISING, handler=new_data_callback)


WIFI_SSID = "BLADE"
WIFI_PASSWORD = "redminote"
WEBSOCKET_URL = ""


pong_rate = 5*1000
last_update = time.ticks_us();
last_pong = time.ticks_ms()

acc = []
gyro = []
mag = []

# print("Calibrating Gyro...")
# sensor.mpu6500.calibrate()
# print("Gyro Calibrated")


# print("Calibrating Magnetometer...")
# sensor.ak8963.calibrate()
# print("Magnetometer Calibrated")

async def connect_wifi():
    global WEBSOCKET_URL
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            print("...")
            await asyncio.sleep(1)
            
    addr = wlan.ifconfig()[2]        
    WEBSOCKET_URL = f"ws://{addr}:8080/ws/socket-server/"        
    print("Connected to Wi-Fi:", wlan.ifconfig())

async def websocket_client():
    global last_update, last_pong, acc, gyro, mag
    ws = AsyncWebsocketClient()
    print("Connecting to WebSocket " , WEBSOCKET_URL)
    await ws.handshake(WEBSOCKET_URL)
    print("Connected to WebSocket server.")
    
    while True:
        #print("Awaiting")
        await new_data.wait()
        
        int_status = sensor.mpu6500._register_char(0x3A)
        sensor.mpu6500._register_char(0x3A, 0x00)
        
        current_time = time.ticks_us()
        elapsed_time = abs(time.ticks_diff(current_time, last_update))
        last_update = current_time
        
        acc = sensor.raw_acceleration
        gyro = sensor.raw_gyro
        mag = sensor.magnetic
        
        t0 = time.ticks_ms()
        data = struct.pack('>6i3d1I', *(acc + gyro + mag + (elapsed_time, )))
        await ws.send(data)
        
        current_time_ms = time.ticks_ms()
        if abs(time.ticks_diff(last_pong, current_time_ms)) > pong_rate:
            #ws.write_frame(OP_PONG)
            await ws.recv()
            last_pong = current_time_ms
            
        print("Latency: ", abs(time.ticks_diff(t0, time.ticks_ms())))
        
        int_status = sensor.mpu6500._register_char(0x3A)
        new_data.clear()
        await asyncio.sleep(0)

async def main():
    await connect_wifi()
    await asyncio.gather(websocket_client())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped.")



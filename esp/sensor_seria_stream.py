from machine import I2C, Timer, UART
import math
import struct
from lib.mpu9250 import MPU9250
from lib.MPU6050 import MPU6050
import time

import socket

i2c = I2C(1, sda=21, scl=22, freq=400000)
#sensor = MPU6050(i2c)
sensor = MPU9250(i2c)
sensor.mpu6500._register_char(0x1A, 0x03)
sensor.mpu6500._register_char(0x1D, 0x03)
 
print(i2c.scan())
 


 
# def read_data(timer):
#     global acc, gyro, mag, temp, elapsed_time, last_update
#     
# 
# tm = Timer(0)
# tm.init(mode = Timer.PERIODIC, period=5, callback=read_data)

# # uart = UART(0, baudrate=100000)
# 
#while True:
     #data = struct.pack(">10f", *(acc + gyro + mag + [temp,]))
#     res = 0;
#      for e in acc:
#          res += e*e
#      print(math.sqrt(res))
#     time.sleep(0.1)


import asyncio as asyncio
import network
import json
from lib.ws import AsyncWebsocketClient
import struct

WIFI_SSID = "BLADE"
WIFI_PASSWORD = "redminote"


WEBSOCKET_URL = ""

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


last_update = time.ticks_us();



async def websocket_client():
    global last_update
    ws = AsyncWebsocketClient()
    print("Connecting to WebSocket " , WEBSOCKET_URL)
    await ws.handshake(WEBSOCKET_URL)
    print("Connected to WebSocket server.")
    while True:
        #t0 = time.ticks_ms()
        
        acc = sensor.raw_acceleration
        gyro = sensor.raw_gyro
        mag = sensor.magnetic
        temp = sensor.temperature
        elapsed_time = abs(time.ticks_diff(time.ticks_us(), last_update))
        last_update = time.ticks_us()
        
        t0 = time.ticks_ms()
        data = struct.pack('>6i3d1I', *(acc + gyro + mag + (elapsed_time, )))
        await ws.send(data)

        #await ws.recv_pong()
        print("Latency1: ", abs(time.ticks_diff(t0, time.ticks_ms())))
        await asyncio.sleep(0.02)

async def main():
    await connect_wifi()
    try:
        await websocket_client()
    except Exception as e:
        print("WebSocket error:", e)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped.")



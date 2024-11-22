import asyncio as asyncio
import network
import json
from lib.ws import AsyncWebsocketClient, OP_PONG
import struct

from machine import I2C, Timer, Pin
import math
import struct
from lib.mpu9250 import MPU9250
from lib.mpu6500 import MPU6500, ACCEL_FS_SEL_16G, GYRO_FS_SEL_1000DPS
import time
import socket


WIFI_SSID = "BLADE"
WIFI_PASSWORD = "redminote"
WEBSOCKET_URL = ""


pong_rate = 5*1000
last_update = -1
last_pong = -1

last_click = 0


pedal = Pin(32, Pin.IN, pull=Pin.PULL_UP)
kick_hit = asyncio.Event()
def pedal_on(pin):
    global last_click, kick_hit
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_click) < 200:
        return
    last_click = current_time
    print("Pedal set", kick_hit.is_set())
    kick_hit.set()
    
pedal.irq(trigger = Pin.IRQ_FALLING, handler=pedal_on)

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

ws = AsyncWebsocketClient()
async def websocket_client():
    global last_update, last_pong, acc, gyro, mag, ws
    print("Connecting to WebSocket " , WEBSOCKET_URL)
    await ws.handshake(WEBSOCKET_URL)
    print("Connected to WebSocket server.")


async def kick_refresh():
    global kick_hit, last_pong
    while(True):
        print("hrtr")
        await kick_hit.wait()
        if ws.sock:
            data = json.dumps({"command": "kick"})
            await ws.send(data)
            print("Sent")
        
        current_time_ms = time.ticks_ms()
        if abs(time.ticks_diff(last_pong, current_time_ms)) > pong_rate:
            #ws.write_frame(OP_PONG)
            await ws.recv()
            last_pong = current_time_ms
            
        kick_hit.clear()
        await asyncio.sleep(0)
        
async def loop():
    while(True):
        await asyncio.sleep(0.1)
        
async def main():
    await connect_wifi()
    await websocket_client()
    await asyncio.gather(loop(), kick_refresh())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped.")




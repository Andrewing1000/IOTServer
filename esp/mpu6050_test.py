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
from MPU6050 import MPU6050
import time
import socket




i2c = I2C(1, sda=21, scl=22, freq=400000)
print(i2c.scan())

sensor6500 = MPU6500(i2c, accel_fs=ACCEL_FS_SEL_16G, gyro_fs=GYRO_FS_SEL_1000DPS)

sensor6500._register_char(0x1A, 0x07) #Dectivate lpf gyro
sensor6500._register_char(0x1D, 0x08) #Deactivate lpf acc
sensor6500._register_char(0x19, 0x01) #Sample divider

sensor6500._register_char(0x38, 0x01) #Activate DR interrupt
current_int_pin_cfg = sensor6500._register_char(0x37) 
current_int_pin_cfg &= 0b11001111 # Clear bits 5 and 4
current_int_pin_cfg |= 0b00110000 # Set desired bits
sensor6500._register_char(0x37, current_int_pin_cfg)

sensor = MPU6050(i2c)

new_data = asyncio.Event()
def new_data_callback(pin):
    new_data.set()

data_timer = Timer(1)
data_timer.init(period=10, mode=Timer.PERIODIC, callback=new_data_callback)


WIFI_SSID = "BLADE"
WIFI_PASSWORD = "redminote"
WEBSOCKET_URL = ""


pong_rate = 5*1000
last_update = -1
last_pong = -1

acc = []
gyro = []
mag = []

last_click = 0


pedal = Pin(32, Pin.IN, pull=Pin.PULL_UP)
kick_hit = asyncio.Event()
def pedal_on(pin):
    global last_click, kick_hit
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_click) < 200:
        return
    last_click = current_time
    print("Pedal set")
    kick_hit.set()

pedal.irq(trigger = Pin.IRQ_FALLING, handler=pedal_on)


print("Calibrating Gyro...")
sensor6500.calibrate()
print("Gyro Calibrated")


# print("Calibrating Magnetometer...")
# sensor.ak8963.calibrate(100)
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

ws = AsyncWebsocketClient()
async def websocket_client():
    global last_update, last_pong, acc, gyro, mag, ws
    print("Connecting to WebSocket " , WEBSOCKET_URL)
    await ws.handshake(WEBSOCKET_URL)
    print("Connected to WebSocket server.")
    
    
async def imu_refresh():
    last_update = time.ticks_us()
    last_pong = time.ticks_ms()
    while True:
        #print("Awaiting")
        await new_data.wait()
        
        current_time = time.ticks_us()
        elapsed_time = abs(time.ticks_diff(current_time, last_update))
        last_update = current_time
        
        acc = sensor.read_accel_data()
        gyro = sensor.read_gyro_data()
        mag = (0,0,0,)
        
        t0 = time.ticks_ms()
        data = struct.pack('>6i3d1I', *(acc + gyro + mag + (elapsed_time, )))
        await ws.send(data)
        
#         print("Latency: ", elapsed_time/1000)
        
        current_time_ms = time.ticks_ms()
        if abs(time.ticks_diff(last_pong, current_time_ms)) > pong_rate:
            #ws.write_frame(OP_PONG)
            await ws.recv()
            last_pong = current_time_ms
            
        #print("Latency: ", abs(time.ticks_diff(t0, time.ticks_ms())))
        
        new_data.clear()
        await asyncio.sleep(0)


async def kick_refresh():
    global kick_hit
    while(True):
        await kick_hit.wait()
        if ws.sock:
            data = json.dumps({"command": "kick"})
            await ws.send(data)
            print("Sent")
        kick_hit.clear()
        await asyncio.sleep(0.2)
        


async def mantente_vivo():
    while(True):
        await asyncio.sleep(0.01)

async def main():
    await connect_wifi()
    await websocket_client()
    await asyncio.gather(imu_refresh(), kick_refresh(), mantente_vivo())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped.")




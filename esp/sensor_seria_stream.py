from machine import I2C, Timer, UART
import math
import struct
from lib.mpu9250 import MPU9250
import time
i2c = I2C(1, sda=21, scl=22, freq=400000)
sensor = MPU9250(i2c)
sensor.mpu6500._register_char(0x1A, 0x03)
sensor.mpu6500._register_char(0x1D, 0x03)

acc = [0, 0, 0]
gyro = [0, 0, 0]
mag = [0, 0, 0]
temp = 0

def read_data(timer):
    global acc, gyro, mag, temp
    acc = sensor.acceleration
    gyro = sensor.gyro
    mag = sensor.magnetic
    temp = sensor.temperature

tm = Timer(0)
tm.init(mode = Timer.PERIODIC, period=5, callback=read_data)

uart = UART(0, baudrate=100000)

while True:
    data = struct.pack(">10f", *(acc + gyro + mag + (temp,)))
    uart.write(data)

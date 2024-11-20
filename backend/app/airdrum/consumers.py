import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .madgwick.madgwick_ahrs import MadgwickAHRS
from .madgwick.queue_filter import FilteredBuffer


import struct
import numpy
import time
import asyncio
from numpy.linalg import norm
class StreamingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'
        self.acc_so = 4096
        self.gyro_so = 32.8
        self.gyro_sf = 0.017453292519943

        self.filter = MadgwickAHRS(sampleperiod=1/100)
        self.acc_filter = FilteredBuffer(cutoff=10, fs=190, type='lowpass',)
        self.mag_filter = FilteredBuffer(cutoff=10, fs=190, type='lowpass')
        self.gyro_filter = FilteredBuffer(cutoff=30, fs=190, type='lowpass')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.accept()
        

    async def receive(self, text_data=None, bytes_data=None):

        if text_data:
            data = json.loads(text_data)
            message = data['command']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': "command_line",
                    'command': message,
                }
            )
            return  


        #t0 = time.time()

        stream = struct.unpack(">6i3d1I", bytes_data)
        acc = stream[0:3]
        gyro = stream[3:6]
        mag = stream[6:9]
        period_us = stream[9]
        period = period_us/1e6

        acc = self.acc_filter.update(acc, period_us)
        gyro = self.gyro_filter.update(gyro, period_us)
        mag = self.mag_filter.update(mag, period_us)
        gyro = tuple(float(value)*self.gyro_sf/self.gyro_so for value in gyro)

        self.filter.samplePeriod = period         
        self.filter.update(gyro, acc, mag)
        roll, pitch, yaw = self.filter.quaternion.to_euler_angles()

        #print("Latency ", time.time()-t0)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sensor_stream',
                'yaw': yaw,
                'pitch': pitch,
                'roll': roll,
            }
        )

    async def command_line(self, event):
        message = event['command']
        await self.send(
            text_data=json.dumps({
                'command': message
            })
        )

    async def sensor_stream(self, event):
        yaw = event['yaw']
        pitch = event['pitch']
        roll = event['roll']

        data = struct.pack(">3d", roll, pitch, yaw)
        await self.send(bytes_data=data)

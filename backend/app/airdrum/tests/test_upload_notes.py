from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse_lazy

from rest_framework.test import APITestCase
from rest_framework import status

from airdrum import models, serializers

import struct
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile

class TestNotes(APITestCase):
    def setUp(self):
        user = {
            'name': 'user',
            'email': 'user@example.com',
            'password': '1234pass',
            'is_active': True, 
            'is_staff': False,
        }

        self.user = get_user_model().objects.create(**user)

    def tearDown(self):
        instances = models.Track.objects.all()
        for instance in instances:
            instance.file.delete()

    def test_upload_track(self):
        self.client.force_authenticate(self.user)

        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as audio_file:
            sine_wave = Sine(100).to_audio_segment(duration=1000)
            sine_wave.export(audio_file.name, format="mp3")
            audio_file.flush()
            audio_file.seek(0)

            data = {
                'name': 'sound1',
                'user': self.user,
                'sound': File(audio_file),
                'private': False,
            }
            sound1 = models.Instrument.objects.create(**data)


        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as audio_file:
            sine_wave = Sine(50).to_audio_segment(duration=1000)
            sine_wave.export(audio_file.name, format="mp3")
            audio_file.flush()
            audio_file.seek(0)

            data = {
                'name': 'sound2',
                'user': self.user,
                'sound': File(audio_file),
                'private': False,
            }
            sound2 = models.Instrument.objects.create(**data)

        data = (
            (0.123, 1, sound1.id),
            (0.344, 0.5, sound2.id),
            (0.123, 1, sound1.id),
            (0.123, 1, sound2.id),
            (0.123, 1, sound1.id),
            (0.23, 1, sound1.id),
        )

        buffer = bytearray()
        buffer += struct.pack('> I', len(data))
        for note in data:
            buffer += struct.pack('> 2f I', *note)
        data = bytes(buffer)

        with tempfile.NamedTemporaryFile(suffix='.bin', delete=True) as temp_file:
            temp_file.write(buffer)
            temp_file.flush()
            temp_file.seek(0)

            payload = {
                'file': File(temp_file),
                'name': 'track_example',
            }
            url = reverse_lazy('airdrum:track-list')
            response = self.client.post(url, data=payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data.get('id', None)
        self.assertTrue(models.Track.objects.filter(id=id).exists())
        self.assertTrue(models.Notes.objects.filter(track__id=id).exists())
        



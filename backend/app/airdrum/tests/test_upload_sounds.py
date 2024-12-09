from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.files import File


from rest_framework.test import APITestCase
from rest_framework import status

from airdrum.models import Instrument, Track

import tempfile
import struct

import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

class SoundUploadTest(APITestCase):
    '''
    Test the feture of user uploaded songs.
    '''
    def setUp(self):
        user = {
            'email': 'user@example.com',
            'password': '1234testo',
            'is_staff': False, 
            'is_active': True,
        }

        self.user = get_user_model().objects.create(**user)

    def tearDown(self):
        instances = Instrument.objects.filter(user=self.user)
        for sound in instances:
            sound.sound.delete(save=False)

    def test_sound_upload(self):
        self.client.force_authenticate(self.user)

        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as audio_file:
            sine_wave = Sine(100).to_audio_segment(duration=1000)
            sine_wave.export(audio_file.name, format="mp3")
            audio_file.flush()
            audio_file.seek(0)

            payload = {
                'sound': File(audio_file),
                'private': True,
                'name': 'test_audio',
            }
            url = reverse_lazy('airdrum:sound-list')
            response  = self.client.post(url, data=payload, format='multipart')

        id = response.data.get('id', None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(id)
        self.assertTrue(Instrument.objects.filter(id=id).exists())

    def test_not_sound_fails(self):
        self.client.force_authenticate(self.user)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as audio_file:
            audio_file.write(b'cocococococ')
            audio_file.flush()

            payload = {
                'sound': File(audio_file),
                'private': True,
                'name': 'test_audio',
            }

            url = reverse_lazy('airdrum:sound-list')
            response = self.client.post(url, data=payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_mp3_fails(self):
        self.client.force_authenticate(self.user)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as audio_file:
            sine_wave = Sine(100).to_audio_segment(duration=1000)
            sine_wave.export(audio_file.name, format="mp3")
            audio_file.flush()

            django_file = File(audio_file) 
            payload = {
                'sound': django_file,
                'private': True,
                'name': 'test_audio',
            }

            url = reverse_lazy('airdrum:sound-list')
            response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tocoto(self):
        self.client.force_authenticate(self.user)
        
        with tempfile.NamedTemporaryFile(delete=True, suffix=".bin", mode="w+b",) as new_file:
            new_file.write(struct.pack("3i 20s", 1, 2, 3, "el mesajito".encode('utf-8')))
            new_file.seek(0)
            data = {'file': new_file}
            url = reverse_lazy("airdrum:testing-testing-action", kwargs={'pk': 1})
            response = self.client.post(url, data=data, format='multipart')
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
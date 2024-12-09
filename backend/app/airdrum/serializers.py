from airdrum.models import Track, Instrument, Notes

from rest_framework import serializers, exceptions, status
from drf_spectacular.utils import extend_schema

import struct
import audioread
from os import path 
import tempfile

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['id', 'name', 'sound', 'user', 'private']
        read_only_fields = ['user', 'id']

    def validate(self, attrs):
        super().validate(attrs)
        file = attrs.get('sound', None)
        file_ext = path.splitext(file.name)[-1]
        
        if not ('mp3' in file_ext) and not ('waw' in file_ext):
            raise exceptions.ValidationError(detail="Formato no soportado", code=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            with tempfile.NamedTemporaryFile(delete=True, suffix=file_ext) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file.flush()

                audio_file = audioread.audio_open(temp_file.name)
                audio_file.close()
            
        except Exception as e:
            raise exceptions.ValidationError(detail= "Archivo incorrecto", code=status.HTTP_400_BAD_REQUEST)
        
        return attrs

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'file', 'user']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        created_track = super().create(validated_data=validated_data)

        file = created_track.file

        data = []
        with open(file.path, mode='r+b') as track_file:
            count = struct.unpack('> I', track_file.read(struct.calcsize('I')))[0]
            row_size = struct.calcsize('> 2f I')
            
            for i in range(count):                 
                data.append(struct.unpack('> 2f I', track_file.read(row_size)))

        for row in data:
            time, volume, sound_id = row
            sound = Instrument.objects.get(id=sound_id)
            Notes.objects.create(time=time, volume=volume, sound=sound, track=created_track)

        return created_track
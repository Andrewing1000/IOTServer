from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import decorators

from airdrum import serializers, models
import struct


def index(request):
    return render(request, 'airdrum/index.html')

def drum_interface(request):
    url = f'{request.get_host()}'
    return render(request, 'airdrum/animacion.html', {'base_url': url})


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = models.Instrument.objects.all()
    serializer_class = serializers.InstrumentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.sound.delete()
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return models.Instrument.objects.filter(user=user) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    

class TrackViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TrackSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return models.Track.objects.filter(user=user)

    def perform_create(self, serializer):
        user =  self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TestingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TrackSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    @decorators.action(methods=['POST', 'PUT'], detail=True, url_path='upload/file')
    def testing_action(self, request, pk=None):
        # print("Just for debuggin purposes !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(repr(request), end="\n\n")

        file = request.data.get('file')
        file1 = request.FILES.get('file')

        # print(file.name)
        # print(file1.name)
        data = b''
        with file.open(mode='r+b') as open_file:
            for chunk in open_file.chunks():
                data += chunk
                chunk = open_file.chunks()
            
            data = struct.unpack("3i 20s", data)
            # print(data[-1].decode('utf-8'))

        return Response(status=status.HTTP_200_OK)

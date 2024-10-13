from django.shortcuts import render
from rest_framework import views, generics, viewsets, exceptions
from tienda.models import Articulo, SineAproximation, CosineAproximation, TangentAproximation, IOTClient
from tienda.serializers import ArticuloSerializer


from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SineSeriesSerializer, CosineSeriesSerializer, TangentSeriesSerializer, IOTClientSerializer

from rest_framework import permissions, authentication


class ArticulosViewSet(viewsets.ModelViewSet):
# Create your views here.
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer


class CreateIOTClient(viewsets.ModelViewSet):
    queryset = IOTClient.objects.all()
    serializer_class = IOTClientSerializer
    authentication_classes = []
    permission_classes = []


class SineSeriesViewSet(viewsets.ModelViewSet):
    queryset = SineAproximation.objects.all()
    authentication_clases = [authentication.TokenAuthentication]
    serializer_class = SineSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if(user.is_superuser): return SineAproximation.objects.all()
        return SineAproximation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CosineSeriesViewSet(viewsets.ModelViewSet):
    queryset = CosineAproximation.objects.all()
    authentication_clases = [authentication.TokenAuthentication]
    serializer_class = CosineSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if(user.is_superuser): return SineAproximation.objects.all()
        return CosineAproximation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TangentSeriesViewSet(viewsets.ModelViewSet):
    queryset = TangentAproximation.objects.all()
    authentication_clases = [authentication.TokenAuthentication]
    serializer_class = TangentSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if(user.is_superuser): return SineAproximation.objects.all()
        return TangentAproximation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class RunSQLQueryView(APIView):
    """
    A view that runs a raw SQL query and returns the result.
    """
    
    def post(self, request, *args, **kwargs):
        query = request.data.get('query', None)
        
        if not query:
            return Response({"error": "No query provided"}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]  # Column names
                results = cursor.fetchall()  # Query results
                
                result_list = [dict(zip(columns, row)) for row in results]

                return Response(result_list, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        




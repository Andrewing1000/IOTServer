from django.shortcuts import render
from rest_framework import views, generics, viewsets, exceptions
from tienda.models import Articulo, SineAproximation, CosineAproximation, TangentAproximation
from tienda.serializers import ArticuloSerializer


from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SineSeriesSerializer, CosineSeriesSerializer, TangentSeriesSerializer

from core.permissions import IsLogged


class ArticulosViewSet(viewsets.ModelViewSet):
# Create your views here.
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

class SineSeriesViewSet(viewsets.ModelViewSet):
    queryset = SineAproximation.objects.all()
    serializer_class = SineSeriesSerializer
    permission_classes = [IsLogged]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CosineSeriesViewSet(viewsets.ModelViewSet):
    queryset = CosineAproximation.objects.all()
    serializer_class = CosineSeriesSerializer
    permission_classes = [IsLogged]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TangentSeriesViewSet(viewsets.ModelViewSet):
    queryset = TangentAproximation.objects.all()
    serializer_class = TangentSeriesSerializer
    permission_classes = [IsLogged]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
    
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
        




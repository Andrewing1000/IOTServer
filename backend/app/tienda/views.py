from django.shortcuts import render
from rest_framework import views, generics, viewsets, exceptions
from tienda.models import Articulo, SineAproximation, CosineAproximation, TangentAproximation, IOTClient, Fibonacci
from tienda.serializers import ArticuloSerializer


from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SineSeriesSerializer, CosineSeriesSerializer, TangentSeriesSerializer, IOTClientSerializer, FibonacciSerializer

from rest_framework import permissions, authentication, status

from random import randrange

class ArticulosViewSet(viewsets.ModelViewSet):
# Create your views here.
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer


class CreateIOTClient(viewsets.ModelViewSet):
    queryset = IOTClient.objects.all()
    serializer_class = IOTClientSerializer
    authentication_classes = []
    permission_classes = []


class FibonacciInterface(views.APIView):

    def get_client_ip(self, request):
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0].strip()
        # else:
        #ip = request.META.get('REMOTE_ADDR')
        print(request.META)
        #ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
        ip = request.META.get('HTTP_CEBOLLIN', None)
        return ip


    def post(self, request, *args, **kwargs):
        terms = list(Fibonacci.objects.all().order_by('n'))
        new_term = None
        ip = self.get_client_ip(request)

        if(len(terms)==0):
            new_term = Fibonacci.objects.create(n=1, fibonacci=1, ip=ip, error=0)
        elif(len(terms)==1):
            new_term = Fibonacci.objects.create(n=2, fibonacci=1, ip=ip, error=0)
        else:
            a = terms[-1]
            b = terms[-2]
            new_value = a.fibonacci+b.fibonacci
            new_error = randrange(-50*(a.n+1)**2, 50*(a.n+1)**2)/100
            new_term = Fibonacci.objects.create(n=a.n+1, fibonacci=new_value, ip=ip, error=new_error)
        return Response(FibonacciSerializer(new_term).data)
    
    def delete(self, request, *args, **kwargs):
        terms=Fibonacci.objects.all().order_by('n')
        last = terms.last()
        if not last: 
            return Response({'error': 'La tabla ya esta vacía'}, status=status.HTTP_404_NOT_FOUND)
        last.delete()
        return Response(status=status.HTTP_200_OK)
    

class FibonacciViewSet(viewsets.ModelViewSet):
    queryset = Fibonacci.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = FibonacciSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_queryset(self):
        return Fibonacci.objects.all().order_by('fibonacci')

    def perform_create(self, serializer):
        request = self.request
        serializer.save(ip=self.get_client_ip(request))
        return super().perform_create(serializer)
    
    def destroy(self, request, *args, **kwars):
        Fibonacci.objects.all().delete()
        return Response(status=status.HTTP_200_OK)
    

class SineSeriesViewSet(viewsets.ModelViewSet):
    queryset = SineAproximation.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = SineSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff: return SineAproximation.objects.all()
        return SineAproximation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = self.request.user
        data['user'] = user
        instance = serializer.update(None, data)
        response_serializer = self.get_serializer(instance)
        
        return Response(response_serializer.data)
   


class CosineSeriesViewSet(viewsets.ModelViewSet):
    queryset = CosineAproximation.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = CosineSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: return CosineAproximation.objects.all()
        return CosineAproximation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = self.request.user
        data['user'] = user
        instance = serializer.update(None, data)
        response_serializer = self.get_serializer(instance)
        
        return Response(response_serializer.data)
   
   
class ActivityView(APIView):
    def get(self, request, *args, **kwargs):
        activity = []
        ips = Fibonacci.objects.values_list('ip', flat=True).distinct()
        for ip in ips:
            if not ip: continue
            sum = len(Fibonacci.objects.filter(ip=ip))
            activity.append({
                'ip': ip,
                'actividad': sum,
            })
        
        return Response(activity)
    

class TangentSeriesViewSet(viewsets.ModelViewSet):
    queryset = TangentAproximation.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = TangentSeriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: return TangentAproximation.objects.all()
        return TangentAproximation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = self.request.user
        data['user'] = user
        instance = serializer.update(None, data)
        response_serializer = self.get_serializer(instance)
        
        return Response(response_serializer.data)
   
   


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
        


def login_view(request):
    base_url = f'{request.scheme}://{request.get_host()}/'
    return render(request, 'tienda/login.html', {'base_url': base_url})

def admin_view(request):
    base_url = f'{request.scheme}://{request.get_host()}/'
    return render(request, 'tienda/admin.html', {'base_url': base_url})

def index_view(request):
    base_url = f'{request.scheme}://{request.get_host()}/'
    return render(request, 'tienda/index.html', {'base_url': base_url})

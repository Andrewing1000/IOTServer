from rest_framework import serializers, exceptions
from tienda.models import Articulo, SineAproximation, CosineAproximation, TangentAproximation, IOTClient, Fibonacci, DrumHit
from user.serializers import UserSerializer

from django.contrib.auth import get_user_model
import random, math


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ['codigo', 'descripcion', 'precio']


MOD = int(1e7+9)
precomputed_fact = [1]


def fact(n):
    global precomputed_fact
    if n < len(precomputed_fact):
        if precomputed_fact[n]: return precomputed_fact[n]
        precomputed_fact[n] = n*fact(n-1) % MOD
        return precomputed_fact[n]

    precomputed_fact += [0] * (n + 1 - len(precomputed_fact))
    return fact(n)


class DrumHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrumHit
        fields = ['value', 'time', 'ip']
        extra_kwargs = {'time': {'read_only': True}, 'ip': {'read_only': True}}


class FibonacciSerializer(serializers.ModelSerializer):
    m = serializers.IntegerField(write_only=True)
    with_error = serializers.SerializerMethodField()
    class Meta:
        model = Fibonacci
        fields = ['n', 'fibonacci', 'error', 'ip', 'with_error', 'm']
        extra_kwargs = {'n': {'read_only':True},
                        'fibonacci' : {'read_only':True},
                        'ip': {'read_only':True}, 
                        'error': {'read_only':True}
                        }
    
    def get_with_error(self, object):
        return object.fibonacci + object.error

    def create(self, validated_data):        
        m = validated_data.pop('m', None)
        ip = validated_data.pop('ip', None)
        terms = list(Fibonacci.objects.order_by('n'))        
        i0 = 0

        a, b = 1, 0
        if len(terms):
            i0 = terms[-1].n
            b=terms[-1].fibonacci
        if len(terms)>1:
            a=terms[-2].fibonacci
        a, b= b, a+b

        for i in range(1, m+1):
            a, b= b, a+b
            Fibonacci.objects.create(
                n=i0+i,
                fibonacci=a,
                ip=ip,
                error = random.randrange(-50, 50)/100
            )
        return Fibonacci.objects.all().last()


class IOTClientSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = IOTClient
        fields = ['pk', 'email', 'password', 'name', 'is_active', 'ip']
        extra_kwargs = {
            'password': {'write_only': True,},
            'ip':{'read_only': True},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Ensure IP is explicitly included even if null
        ret['ip'] = instance.iotclient.ip if hasattr(instance, 'iotclient') else ''
        return ret

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        iotclient = IOTClient(**validated_data)
        iotclient.email = validated_data.get("email")
        iotclient.set_password(validated_data.get("password"))
        #iotclient.name = validated_data.get("name")
        iotclient.save()
        return iotclient

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user



class SineSeriesSerializer(serializers.ModelSerializer):
    with_error = serializers.SerializerMethodField()
    m = serializers.IntegerField(write_only=True)
    user = IOTClientSerializer(required=False)
    class Meta:
        model = SineAproximation
        fields = ['n', 'term' ,'error', 'with_error', 'm', 'user']
        extra_kwargs = {
            'n':{'read_only': True},
            'term':{'read_only':True},
            'error':{'read_only':True},
            'with_error':{'read_only':True},
            'm':{'write_only': True,},
            'user':{'read_only'},
        }


    def create(self, validated_data):
        m = validated_data.pop('m', None)
        if not m: 
            raise exceptions.NotAcceptable('Ingrese el numero de términos')

        instances = []
        d = 1
        for i in range(1, m+1):
            instance = SineAproximation(
                n=i,
                term=math.sin(i*d),
                error=random.randrange(-50, 50)/100,
                user=validated_data.get('user'),
            )
            instances.append(instance)
        SineAproximation.objects.all().delete()
        SineAproximation.objects.bulk_create(instances)
        return instances[-1]
            

    def update(self, instance, validated_data):
        m = validated_data.get('m', None)
        if not m: 
            raise exceptions.NotAcceptable('Ingrese el numero de terminos')
        m0 = SineAproximation.objects.values_list('n', flat=True).last()
        if not m0:
            m0=0
        instances = []
        d = 1
        for i in range(m0+1, m0+m+1):
            instance=SineAproximation(
                n=i,
                term=math.sin(i*d),
                error=random.randrange(-50, 50)/100,
                user=validated_data.get('user'),

            )
            instances.append(instance)

        SineAproximation.objects.bulk_create(instances)
        return instance

    def get_with_error(self, obj):
        return obj.term + obj.error
    

    

class CosineSeriesSerializer(serializers.ModelSerializer):
    with_error = serializers.SerializerMethodField()
    m = serializers.IntegerField(write_only=True)
    user = IOTClientSerializer(required=False)
    class Meta:
        model = CosineAproximation
        fields = ['n', 'term' ,'error', 'with_error', 'm', 'user']
        extra_kwargs = {
            'n':{'read_only': True},
            'term':{'read_only':True},
            'error':{'read_only':True},
            'with_error':{'read_only':True},
            'm':{'write_only':True},
            'user':{'read_only'},
        }

    def create(self, validated_data):
        m = validated_data.get('m', None)
        if not m: 
            raise exceptions.NotAcceptable('Ingrese el numero de términos')

        instances = []
        d = 1
        for i in range(1, m+1):
            instance = CosineAproximation(
                n=i,
                term=math.cos(i*d),
                error=random.randrange(-50, 50)/100,
                user=validated_data.get('user'),
            )
            instances.append(instance)

        
        CosineAproximation.objects.all().delete()
        CosineAproximation.objects.bulk_create(instances)
        return instances[-1]
            

    def update(self, instance, validated_data):
        m = validated_data.get('m', None)
        m0 = CosineAproximation.objects.values_list('n', flat=True).last()
        if not m0:
            m0=0
        instances = []
        d = 1
        for i in range(m0+1, m0+m+1):
            instance=CosineAproximation(
                n=i,
                term=math.cos(i*d),
                error=random.randrange(-50, 50)/100,
                user=validated_data.get('user'),
            )
            instances.append(instance)

        CosineAproximation.objects.bulk_create(instances)
        return instance

    def get_with_error(self, obj):
        return obj.term + obj.error
    
class TangentSeriesSerializer(serializers.ModelSerializer):
    with_error = serializers.SerializerMethodField()
    m = serializers.IntegerField(write_only=True)
    user = IOTClientSerializer(required=False)
    class Meta:
        model = TangentAproximation
        fields = ['n', 'term', 'error', 'with_error', 'm', 'user']
        extra_kwargs = {
            'n':{'read_only': True},
            'term': {'read_only': True},
            'error': {'read_only': True},
            'with_error': {'read_only': True},
            'm': {'write_only': True},
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        m = validated_data.get('m', None)

        instances = []
        user = validated_data.get('user')  # Assume `user` comes from validated data

        d = 0.05
        for i in range(1, m + 1):
            # Tangent Taylor series term calculation
            term = self.calculate_tangent_term(i)
            instance = TangentAproximation(
                n=i,
                term = math.tan(i*d),
                error=random.uniform(-30, 30),  # Using `uniform` to avoid hard range
                user=user,
            )
            instances.append(instance)

        
        TangentAproximation.objects.all().delete()
        TangentAproximation.objects.bulk_create(instances)
        return instances[-1]

    def update(self, instance, validated_data):
        m = validated_data.get('m', None)
        m0 = TangentAproximation.objects.values_list('n', flat=True).last() or 0

        instances = []
        d = 0.05
        for i in range(m0 + 1, m0 + m + 1):
            # Tangent Taylor series term calculation
            term = self.calculate_tangent_term(i)
            new_instance = TangentAproximation(
                n=i,
                term=math.tan(i*d),
                error=random.uniform(-30, 30)/50,
                user=validated_data.get('user'),
            )
            instances.append(new_instance)

        
        TangentAproximation.objects.bulk_create(instances)
        return instances[-1] if instances else instance

    def get_with_error(self, obj):
        if obj.term is not None and obj.error is not None:
            return obj.term + obj.error
        return None

    def calculate_tangent_term(self, n):
        return ((-1) ** (n - 1)) * (2 ** (2 * n)) * (2 ** n - 1) / fact(n)

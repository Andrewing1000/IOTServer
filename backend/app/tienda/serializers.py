from rest_framework import serializers, exceptions
from tienda.models import Articulo, SineAproximation, CosineAproximation, TangentAproximation
import random


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

class SineSeriesSerializer(serializers.ModelSerializer):
    with_error = serializers.SerializerMethodField()
    m = serializers.IntegerField()
    class Meta:
        model = SineAproximation
        fields = ['n', 'term' ,'error', 'with_error', 'm']
        extra_kwargs = {
            'term':{'read_only':True},
            'error':{'read_only':True},
            'with_error':{'read_only':True},
            'm':{'write_only':True}
        }

    def create(self, validated_data):
        m = validated_data.get('m', None)
        if not m: 
            raise exceptions.NotAcceptable('Ingrese el numero de términos')

        instances = []
        for i in range(1, m+1):
            instance = SineAproximation(
                n=i,
                term=1.0/fact(2*i-1),
                error=random.randrange(-100, 100)/100,
                user=validated_data.get('user'),
            )
            instances.append(instance)

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
        for i in range(m0+1, m0+m+1):
            instance=SineAproximation(
                n=i,
                term=1.0/fact(2*i-1),
                error=random.randrange(-100, 100)/100
            )
            instances.append(instance)

        SineAproximation.objects.bulk_create(instances)
        return instance

    def get_with_error(self, obj):
        return obj.term + obj.error
    

    

class CosineSeriesSerializer(serializers.ModelSerializer):
    with_error = serializers.SerializerMethodField()
    class Meta:
        model = CosineAproximation
        fields = ['n', 'term' ,'error', 'with_error', 'm']
        extra_kwargs = {
            'term':{'read_only':True},
            'error':{'read_only':True},
            'with_error':{'read_only':True},
            'm':{'write_only':True}
        }

    def create(self, validated_data):
        m = validated_data.get('m', None)
        if not m: 
            raise exceptions.NotAcceptable('Ingrese el numero de términos')

        instances = []
        for i in range(1, m+1):
            instance = CosineAproximation(
                n=i,
                term=1.0/fact(2*i-1),
                error=random.randrange(-100, 100)/100,
                user=validated_data.get('user'),
            )
            instances.append(instance)

        CosineAproximation.objects.bulk_create(instances)
        return instances[-1]
            

    def update(self, instance, validated_data):
        m = validated_data.get('m', None)
        if not m: 
            raise exceptions.NotAcceptable('Ingrese el numero de terminos')
        m0 = CosineAproximation.objects.values_list('n', flat=True).last()
        if not m0:
            m0=0
        instances = []
        for i in range(m0+1, m0+m+1):
            instance=CosineAproximation(
                n=i,
                term=1.0/fact(2*i),
                error=random.randrange(-100, 100)/100
            )
            instances.append(instance)

        CosineAproximation.objects.bulk_create(instances)
        return instance

    def get_with_error(self, obj):
        return obj.term + obj.error
    
class TangentSeriesSerializer(serializers.ModelSerializer):
    with_error = serializers.SerializerMethodField()
    
    class Meta:
        model = TangentAproximation
        fields = ['n', 'term', 'error', 'with_error', 'm']
        extra_kwargs = {
            'term': {'read_only': True},
            'error': {'read_only': True},
            'with_error': {'read_only': True},
            'm': {'write_only': True},
        }

    def create(self, validated_data):
        m = validated_data.get('m', None)
        if not m:
            raise exceptions.NotAcceptable('Ingrese el número de términos')

        instances = []
        user = validated_data.get('user')  # Assume `user` comes from validated data

        for i in range(1, m + 1):
            # Tangent Taylor series term calculation
            term = self.calculate_tangent_term(i)
            instance = TangentAproximation(
                n=i,
                term=term,
                error=random.uniform(-1, 1),  # Using `uniform` to avoid hard range
                user=user,
            )
            instances.append(instance)

        TangentAproximation.objects.bulk_create(instances)
        return instances[-1]

    def update(self, instance, validated_data):
        m = validated_data.get('m', None)
        if not m:
            raise exceptions.NotAcceptable('Ingrese el número de términos')

        m0 = TangentAproximation.objects.values_list('n', flat=True).last() or 0

        instances = []
        for i in range(m0 + 1, m0 + m + 1):
            # Tangent Taylor series term calculation
            term = self.calculate_tangent_term(i)
            new_instance = TangentAproximation(
                n=i,
                term=term,
                error=random.uniform(-1, 1),
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

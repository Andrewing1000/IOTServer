from django.db import models
from django.contrib.auth import get_user_model
from core.models import User 

class Articulo(models.Model):
    codigo = models.IntegerField()
    descripcion = models.TextField()
    precio = models.FloatField()

class Fibonacci(models.Model):
    fibonaccic = models.FloatField()
    conruido = models.FloatField()
    error = models.FloatField()

class SineAproximation(models.Model):
    n = models.IntegerField(
        null=False,
        blank=False,
    )
    term = models.FloatField(
        null=False,
    )
    error = models.FloatField(
        null=False,
    )
    user = models.ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

class CosineAproximation(models.Model):
    n = models.IntegerField(
        null=False,
        blank=False,
    )
    term = models.FloatField(
        null=False
    )
    error = models.FloatField(
        null=False,
    )
    user = models.ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

class TangentAproximation(models.Model):
    n = models.IntegerField(
        null=False,
        blank=False,
    )
    term = models.FloatField(
        null=False
    )
    error = models.FloatField(
        null=False,
    )
    user = models.ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

class IOTClient(User):
    ip = models.CharField(max_length=255, blank=True, null=True)

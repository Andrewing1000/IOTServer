from django.db import models
from django.contrib.auth import get_user_model
from core.models import User 

class Articulo(models.Model):
    codigo = models.IntegerField()
    descripcion = models.TextField()
    precio = models.FloatField()


class DrumHit(models.Model):
    time = models.TimeField()
    value = models.FloatField()
    ip = models.CharField(
        max_length=255,
        null=True,
        blank=True)

class Fibonacci(models.Model):
    n = models.IntegerField(
        null=False,
        blank=False,
        default=1,
        unique=True,
    )
    fibonacci = models.FloatField(
        null=False,
        blank=False,
    )
    error = models.FloatField(
        null=False,
        blank=False,
    )
    ip = models.CharField(
        max_length=30,
        null=True, 
        blank=True,
    )

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

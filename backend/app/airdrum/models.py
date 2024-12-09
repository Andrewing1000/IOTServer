from django.db import models

from uuid import uuid4
from os import path 

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

def create_file_path(intstance, filename):
    ext = path.splitext(filename)[-1]
    return f'{uuid4()}{ext}'


class Track(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=create_file_path)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=False, 
        null=False, 
        default=1,
    )

class Instrument(models.Model):
    name = models.CharField(max_length=255) 
    sound = models.FileField(upload_to=create_file_path)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=False, 
        null=False, 
    )
    private  =  models.BooleanField(
        blank=False,
        null=False,
        default=True,
    )

class Notes(models.Model):
    track = models.ForeignKey(
        Track,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        default=0,
        related_name='notes',
    )
    time = models.DecimalField(
        max_digits=1000,
        decimal_places=100,
        validators=[
            MinValueValidator(limit_value=0)
        ],
        blank=False, 
        null=False,
        default=0,
    )
    sound = models.ForeignKey(
        Instrument,
        blank=False, 
        null=False, 
        on_delete=models.RESTRICT,
        default=0,    
    )
    volume = models.DecimalField(
        max_digits=100,
        decimal_places=6,
        validators=[
            MaxValueValidator(limit_value=1),
            MinValueValidator(limit_value=0),
        ]
    )









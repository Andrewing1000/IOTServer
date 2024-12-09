# Generated by Django 3.2.25 on 2024-12-08 21:52

import airdrum.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sound', models.FileField(upload_to=airdrum.models.create_file_path)),
                ('private', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=airdrum.models.create_file_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DecimalField(decimal_places=6, max_digits=100)),
                ('volume', models.DecimalField(decimal_places=6, max_digits=100, validators=[django.core.validators.MaxValueValidator(limit_value=1), django.core.validators.MinValueValidator(limit_value=0)])),
                ('sound', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='airdrum.instrument')),
                ('track', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, related_name='notes', to='airdrum.track')),
            ],
        ),
    ]
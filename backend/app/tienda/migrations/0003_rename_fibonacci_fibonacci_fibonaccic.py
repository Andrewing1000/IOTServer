# Generated by Django 3.2.25 on 2024-09-30 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_fibonacci'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fibonacci',
            old_name='Fibonacci',
            new_name='Fibonaccic',
        ),
    ]

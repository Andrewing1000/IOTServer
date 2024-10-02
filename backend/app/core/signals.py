# In your app's signals.py file
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from core.models import Role

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    if sender.name == 'core':
        Role.createRoles()
        
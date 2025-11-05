from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .tasks import create_user_credits_task

@receiver(post_save, sender=User)
def create_user_credits(sender, instance, created, **kwargs):
    if created:
        create_user_credits_task.delay(instance.id)
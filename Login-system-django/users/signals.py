from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def send_password_mail(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#                 'Code',
#                 f'{instance.rand_number}',
#                 settings.EMAIL_HOST_USER,
#                 [instance.email],)
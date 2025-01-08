from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def send_sms_after_registration(sender, instance, created, **kwargs):
    """
    Отправка SMS после регистрации нового пользователя.
    """
    if created:
        instance.generate_otp()
        instance.send_mock_sms()


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Payment


@receiver(post_save, sender=User)
def send_sms_after_registration(sender, instance, created, **kwargs):
    """Отправка SMS после регистрации нового пользователя"""
    if created and not instance.is_otp_sent:
        instance.generate_otp()
        instance.send_mock_sms()
        instance.is_otp_sent = True
        instance.save()


@receiver(post_save, sender=Payment)
def update_subscription(sender, instance, created, **kwargs):
    """Если платеж успешно завершен, обновляем статус подписки пользователя"""
    if created and instance.status == 'paid':
        instance.user.is_subscribed = True
        instance.user.save()

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from users.utils import generate_otp, send_mock_sms, verify_otp
from users.validators import validate_phone_number
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя')
    phone = PhoneNumberField(max_length=20, unique=True, verbose_name='Номер телефона',
                             help_text='Введите номер телефона', validators=[validate_phone_number])
    email = models.EmailField(unique=True, verbose_name='Электронная почта', help_text='Введите электронную почту')
    tg_nick = models.CharField(max_length=50, unique=True, verbose_name='Ник в Telegram',
                               help_text='Введите ник в Telegram', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', help_text='Выберите изображение', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка')
    otp_code = models.CharField(max_length=6, verbose_name='Код подтверждения', help_text='Код для подтверждения',
                                **NULLABLE)
    otp_created_at = models.DateTimeField(verbose_name='Время генерации OTP', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.phone} - {self.name}'

    def generate_otp(self):
        """Генерация и сохранение OTP"""
        self.otp_code = generate_otp()
        self.otp_created_at = now()
        self.save()

    def send_mock_sms(self):
        """Имитация отправки SMS"""
        send_mock_sms(self.phone, self.otp_code)

    def verify_otp(self, otp):
        """Проверка введенного кода"""
        is_valid, message = verify_otp(self.otp_code, self.otp_created_at, otp)
        if is_valid:
            self.otp_code = None  # Код подтвержден, удаляем его
            self.save()
        return is_valid, message

from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона',
                             help_text='Введите номер телефона')
    email = models.EmailField(unique=True, verbose_name='Электронная почта', help_text='Введите электронную почту')
    tg_nick = models.CharField(max_length=50, unique=True, verbose_name='Ник в Telegram',
                               help_text='Введите ник в Telegram', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', help_text='Выберите изображение', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.phone} - {self.name}'

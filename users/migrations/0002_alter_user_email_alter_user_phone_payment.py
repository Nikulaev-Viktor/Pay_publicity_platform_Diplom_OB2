# Generated by Django 5.1.4 on 2025-01-17 18:39

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, help_text='Введите электронную почту', max_length=254, null=True, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Введите номер телефона', max_length=20, region=None, unique=True, verbose_name='Номер телефона'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания платежа', verbose_name='Дата создания')),
                ('stripe_session_id', models.CharField(max_length=255, verbose_name='ID сессии Stripe')),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('paid', 'Оплачено'), ('failed', 'Ошибка')], default='pending', max_length=50, verbose_name='Статус платежа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]

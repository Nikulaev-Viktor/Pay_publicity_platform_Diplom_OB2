# Generated by Django 5.1.4 on 2025-01-23 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_otp_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, help_text='Введите электронную почту', max_length=254, null=True, verbose_name='Электронная почта'),
        ),
    ]

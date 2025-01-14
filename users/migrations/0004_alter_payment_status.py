# Generated by Django 5.1.4 on 2025-01-14 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Ожидание'), ('paid', 'Оплачено'), ('failed', 'Ошибка')], default='pending', max_length=50, verbose_name='Статус платежа'),
        ),
    ]

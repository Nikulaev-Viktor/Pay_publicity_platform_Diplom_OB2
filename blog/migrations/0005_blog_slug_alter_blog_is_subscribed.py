# Generated by Django 5.1.4 on 2025-01-11 16:43

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blog_is_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='title', unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='is_subscribed',
            field=models.BooleanField(default=False, help_text='Доступ после оплаты', verbose_name='Подписка'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_category_alter_blog_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_subscribed',
            field=models.BooleanField(default=False, help_text='Платная статья', verbose_name='Подписка'),
        ),
    ]

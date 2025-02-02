# Generated by Django 5.1.4 on 2025-01-12 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_slug_alter_blog_is_subscribed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': [('can_view_blog', 'Can view blog'), ('can_change_blog', 'Can change blog'), ('can_delete_blog', 'Can delete blog')], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='blog.category', verbose_name='Категория'),
        ),
    ]

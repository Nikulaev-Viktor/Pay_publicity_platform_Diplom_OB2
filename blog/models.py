from django.db import models
from autoslug import AutoSlugField
from users.models import NULLABLE, User


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория', help_text='Введите название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок', help_text='Введите заголовок')
    content = models.TextField(verbose_name='Содержание', help_text='Введите текст статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', help_text='Выберите изображение',
                              **NULLABLE)
    slug = AutoSlugField(populate_from='title', unique=True, verbose_name='Slug', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', help_text='Дата создания статьи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения',
                                      help_text='Дата последнего изменения статьи')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, related_name='blogs')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE,
                                 related_name="categories")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка', help_text='Доступ после оплаты')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        permissions = [
            ('can_view_blog', 'Can view blog'),
            ('can_change_blog', 'Can change blog'),
            ('can_delete_blog', 'Can delete blog'),
        ]





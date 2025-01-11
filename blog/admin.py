from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'is_published', 'views_count', 'created_at')

    list_filter = ('is_published',)
    search_fields = ('title', 'content',)
    prepopulated_fields = {'slug': ('title',)}

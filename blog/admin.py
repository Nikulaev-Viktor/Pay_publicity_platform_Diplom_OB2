from django.contrib import admin
from blog.models import Blog, Category


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'is_published', 'views_count', 'created_at')
    list_filter = ('is_published', 'is_subscribed', 'category')
    search_fields = ('title', 'content',)
    exclude = ('slug',)
    readonly_fields = ('slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)





from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from blog.models import Blog
from users.models import User


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'blog/index.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unique_authors'] = Blog.objects.values('author').distinct().count()
        context['total_posts'] = Blog.objects.all().count()
        context['unique_members'] = User.objects.filter(is_active=True).count()
        context['random_posts'] = Blog.objects.all().order_by('?')[:3]
        return context


class ContactsView(View):
    """Контроллер страницы контактов"""

    def get(self, request, *args, **kwargs):
        """Обработка GET-запроса"""
        context = {
            'title': 'Контакты',
        }
        return render(request, 'blog/contacts.html', context)

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса"""
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}: ({phone}) - {message}')

        context = {
            'title': 'Контакты'
        }
        return render(request, 'blog/contacts.html', context)


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер создания статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published', 'is_subscribed', 'category', 'author')
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_add_blog'
    extra_context = {'title': 'Создание статьи'}

    def has_permission(self):
        """Добавляем проверку на суперпользователя"""
        return self.request.user.is_superuser or super().has_permission()

    def form_valid(self, form):
        new_mat = form.save()
        user = self.request.user
        new_mat.author = user
        new_mat.save()
        return super().form_valid(form)


class BlogListView(PermissionRequiredMixin, ListView):
    """Контроллер просмотра статей"""
    model = Blog
    template_name = 'blog/blog_list.html'
    paginate_by = 10
    permission_required = 'blog.can_view_blog'
    extra_context = {'title': 'Список статей'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список статей'
        context['is_subscribed'] = self.request.user.is_subscribed
        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Контроллер просмотра статьи"""

    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        blog.views_count += 1
        blog.save()
        context = {'blog': blog}
        return render(request, 'blog/blog_detail.html', context)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер редактирования статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published', 'is_subscribed', 'category')
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_change_blog'
    extra_context = {'title': 'Редактирование статьи'}


def toggle_activity(request, pk):
    """Функция переключения активности статьи"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect(reverse('blog:list'))


def CreateBlogList(request):
    blog_list = Blog.objects.all()
    context = {
        'object_list': blog_list,

    }
    return render(request, 'blog/toggle.html', context)


def toggle_subscription(request, pk):
    """Функция переключения подписки на статью"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_subscribed:
        blog_item.is_subscribed = False
    else:
        blog_item.is_subscribed = True
    blog_item.save()
    return redirect(reverse('blog:list'))


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_delete_blog'
    extra_context = {'title': 'Удаление статьи'}

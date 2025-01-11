from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from blog.models import Blog


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'blog/index.html'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
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
    fields = ('title', 'content', 'image', 'is_published', 'is_subscribed')
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blog'
    extra_context = {'title': 'Создание статьи'}

    def form_valid(self, form):
        new_mat = form.save()
        user = self.request.user
        new_mat.author = user
        new_mat.save()
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    """Контроллер просмотра статей"""
    model = Blog
    template_name = 'blog/blog_list.html'
    paginate_by = 10
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


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Контроллер редактирования статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published', 'is_subscribed', 'category', 'is_subscribed')
    success_url = reverse_lazy('blog:list')
    extra_context = {'title': 'Редактирование статьи'}


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Контроллер удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'
    extra_context = {'title': 'Удаление статьи'}


def toggle_activity(request, pk):
    """Функция переключения активности статьи"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()
    return redirect(reverse('blog:list'))


def toggle_subscription(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    blog_item.is_subscribed = not blog_item.is_subscribed
    blog_item.save()
    return redirect(reverse('blog:list'))

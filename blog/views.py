from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from blog.models import Blog, Category
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
        context['random_posts'] = Blog.objects.all().order_by('?')[:4]

        if self.request.user.is_authenticated:
            context['is_subscribed'] = self.request.user.is_subscribed
        else:
            context['is_subscribed'] = False

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


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published', 'is_subscribed', 'category')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {'title': 'Создание статьи'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogListView(ListView):
    """Контроллер просмотра статей"""
    model = Blog
    template_name = 'blog/blog_list.html'
    paginate_by = 9
    extra_context = {'title': 'Список статей'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список статей'

        if self.request.user.is_authenticated:
            context['is_subscribed'] = self.request.user.is_subscribed
        else:
            context['is_subscribed'] = False

        return context


class BlogDetailView(DetailView):
    """Контроллер просмотра статьи"""
    model = Blog
    template_name = 'blog/blog_detail.html'
    extra_context = {'title': 'Просмотр статьи'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_subscribed'] = self.request.user.is_subscribed
        else:
            context['is_subscribed'] = False

        return context


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования статьи"""
    model = Blog
    fields = ('title', 'content', 'image', 'is_published', 'is_subscribed', 'category',)
    success_url = reverse_lazy('blog:blog_list')
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


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {'title': 'Удаление статьи'}


class CategoryListView(ListView):
    """Контроллер просмотра статей по категориям"""
    model = Category
    template_name = 'blog/category_list.html'
    paginate_by = 10
    extra_context = {'title': 'Список статей по категориям'}


class CategoryDetailView(ListView):
    """Контроллер просмотра статей по категориям"""
    model = Blog
    template_name = 'blog/category_detail.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Blog.objects.filter(category__id=category_id, is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['category'] = Category.objects.get(id=category_id)
        if self.request.user.is_authenticated:
            context['is_subscribed'] = self.request.user.is_subscribed
        else:
            context['is_subscribed'] = False
        return context

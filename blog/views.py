from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View


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


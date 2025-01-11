from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда создания суперпользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@example.ru', phone='+79779177963', name='Admin')
        user.set_password('123qwe456')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

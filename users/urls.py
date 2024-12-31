from django.urls import path, include
from users.apps import UsersConfig


app_name = UsersConfig.name
urlpatterns = [
    path('',),
]
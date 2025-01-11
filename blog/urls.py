from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import IndexView, ContactsView

app_name = BlogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

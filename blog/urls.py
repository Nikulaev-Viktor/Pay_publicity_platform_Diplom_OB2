from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import IndexView, ContactsView, BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, \
    toggle_activity, BlogDeleteView, toggle_subscription, CreateBlogList

app_name = BlogConfig.name

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('contacts/', ContactsView.as_view(), name='contacts'),
                  path('create/', BlogCreateView.as_view(), name='create'),
                  path('blog_list/', BlogListView.as_view(), name='blog_list'),
                  path('detail/<int:pk>/', BlogDetailView.as_view(), name='detail'),
                  path('edit/<int:pk>/', BlogUpdateView.as_view(), name='update'),
                  path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
                  path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
                  path('subscription/<int:pk>/', toggle_subscription, name='toggle_subscription'),
                  path('toggle/', CreateBlogList, name='toggle'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

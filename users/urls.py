from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from users.views import ProfileView, CreateUserView, UserDeleteView, UserOTPVerifyView, UserDeleteConfirmationView

app_name = UsersConfig.name
urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('OTP_verify/', UserOTPVerifyView.as_view(template_name='users/otp_verify.html'), name='otp_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user_delete"),
    path('users/<int:pk>/confirm_delete', UserDeleteConfirmationView.as_view(), name="user_confirm_delete"),




]
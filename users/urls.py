from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from users.views import ProfileView, CreateUserView, UserDeleteView, UserOTPVerifyView, UserDeleteConfirmationView, \
    PasswordResetRequestView, PasswordResetVerifyView, NewPasswordView, SubscribeView

app_name = UsersConfig.name
urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('OTP_verify/<int:pk>/', UserOTPVerifyView.as_view(template_name='users/otp_verify.html'), name='otp_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/<int:pk>/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),
    path('new_password/<int:pk>/', NewPasswordView.as_view(), name='new_password'),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user_delete"),
    path('users/<int:pk>/confirm_delete', UserDeleteConfirmationView.as_view(), name="user_confirm_delete"),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),




]
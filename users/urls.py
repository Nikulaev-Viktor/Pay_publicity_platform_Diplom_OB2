from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from users.views import ProfileView, CreateUserView, UserDeleteView, UserOTPVerifyView, UserDeleteConfirmationView, \
    PasswordResetRequestView, NewPasswordView, SubscribeView, CreatePaymentView, \
    SubscribeSuccessView, SubscribeCancelView

app_name = UsersConfig.name
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('otp_verify/<str:action>/<int:pk>/', UserOTPVerifyView.as_view(), name='otp_verify'),
    path('new_password/<int:pk>/', NewPasswordView.as_view(), name='new_password'),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user_delete"),
    path('users/<int:pk>/confirm_delete', UserDeleteConfirmationView.as_view(), name="user_confirm_delete"),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('create-payment/', CreatePaymentView.as_view(), name='create_payment'),
    path('subscribe/success/', SubscribeSuccessView.as_view(), name='subscribe_success'),
    path('subscribe/cancel/', SubscribeCancelView.as_view(), name='subscribe_cancel'),




]
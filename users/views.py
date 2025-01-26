from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, FormView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from users.forms import UserRegisterForm, OTPVerificationForm, UserLoginForm, UserProfileForm, PasswordResetRequestForm, \
    NewPasswordForm
from users.models import User, Payment
from users.services import create_stripe_price, create_stripe_session, check_payment_status
from django.http import HttpResponseForbidden


class CreateUserView(CreateView):
    """Контроллер создания пользователя"""
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация нового пользователя'}

    def form_valid(self, form):
        """Сохраняем пользователя и перенаправляем на страницу подтверждения OTP"""
        user = form.save(commit=False)
        user.is_active = False  # Устанавливаем пользователя неактивным
        user.save()  # Сохранили пользователя, сигнал `post_save` вызовет отправку OTP
        messages.info(self.request, 'Введите OTP для подтверждения.')
        return redirect('users:otp_verify', action='register', pk=user.pk)


class UserOTPVerifyView(FormView):
    """Подтверждение OTP после регистрации"""
    template_name = 'users/otp_verify.html'
    form_class = OTPVerificationForm

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        otp = form.cleaned_data['otp']

        # Проверка OTP
        otp_valid, otp_message = user.verify_otp(otp)
        if not otp_valid:
            form.add_error('otp', otp_message)
            return self.form_invalid(form)

        # Если OTP верный, проверяем действие
        action = self.kwargs.get('action')
        if action == 'password_reset':
            messages.success(self.request, 'OTP успешно подтвержден. Введите новый пароль.')
            return redirect('users:new_password', pk=user.pk)
        elif action == 'register':
            user.is_active = True
            user.save()
            messages.success(self.request, 'Регистрация завершена! Теперь вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(self.request, 'Неизвестное действие.')
            return redirect('users:login')


class UserLoginView(LoginView):
    """Контроллер логина"""
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер профиля"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления пользователя"""
    model = User
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('users:login')


class UserDeleteConfirmationView(View):
    """Контроллер подтверждения удаления пользователя"""

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'users/confirm_delete.html', {'user': user})


class PasswordResetRequestView(FormView):
    """Контроллер запроса на сброс пароля"""
    template_name = 'users/password_reset_request.html'
    form_class = PasswordResetRequestForm

    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        user = User.objects.filter(phone=phone).first()
        if not user:
            form.add_error('phone', 'Пользователь с таким номером не найден.')
            return self.form_invalid(form)

        user.generate_otp()
        user.send_mock_sms()
        user.is_otp_sent = True
        user.save()
        messages.info(self.request, 'OTP отправлен на ваш номер телефона.')
        return redirect('users:otp_verify', action='password_reset', pk=user.pk)


class NewPasswordView(FormView):
    """Контроллер ввода нового пароля"""
    template_name = 'users/new_password.html'
    form_class = NewPasswordForm
    extra_context = {'title': 'Создание нового пароля'}

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['user'] = user
        return context

    def form_valid(self, form):
        new_password = form.cleaned_data['new_password1']
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        user.set_password(new_password)
        user.save()
        messages.success(self.request, 'Пароль успешно изменен.')
        return redirect('users:login')


class SubscribeView(TemplateView):
    """Контроллер подписки"""
    template_name = 'users/subscribe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление подписки'
        return context


class CreatePaymentView(View, HttpResponseForbidden):
    """Контроллер создания платежа для подписки"""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Вы должны быть авторизованы для выполнения этой операции.")
        price = create_stripe_price()
        session_id, session_url = create_stripe_session(price)

        Payment.objects.create(
            user=request.user,
            amount=500,
            stripe_session_id=session_id,
            status='pending',
        )
        return redirect(session_url)


class SubscribeSuccessView(TemplateView):
    template_name = "users/payment_success.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        check_payment_status(user)
        return super().get(request, *args, **kwargs)


class SubscribeCancelView(TemplateView):
    template_name = "users/payment_cancel.html"

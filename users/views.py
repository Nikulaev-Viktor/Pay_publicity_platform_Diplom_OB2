import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, FormView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from users.forms import UserRegisterForm, OTPVerificationForm, UserLoginForm, UserProfileForm, PasswordResetRequestForm, \
    NewPasswordForm
from users.models import User, Payment
from users.services import create_stripe_price, create_stripe_session


class CreateUserView(CreateView):
    """Контроллер создания пользователя"""
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Сохраняем пользователя и перенаправляем на страницу подтверждения OTP"""
        user = form.save(commit=False)
        user.is_active = False  # Устанавливаем пользователя неактивным
        user.save()  # Сохраняем пользователя, сигнал `post_save` вызовет отправку OTP
        messages.info(self.request, 'Введите OTP для подтверждения.')
        return redirect('users:otp_verify', pk=user.pk)
        # return HttpResponseRedirect(reverse_lazy('users:otp_verify', kwargs={'pk': user.pk}))


class UserOTPVerifyView(FormView):
    """Проверка OTP"""
    template_name = 'users/otp_verify.html'
    form_class = OTPVerificationForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение OTP'
        logging.debug(f"Context for OTP verify view: {context}")
        return context

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        otp = form.cleaned_data['otp']
        is_valid, message = user.verify_otp(otp)
        if is_valid:
            user.is_active = True
            user.save()
            messages.success(self.request, 'Подтверждение успешно!')
            return redirect('users:login')
        else:
            messages.error(self.request, message)
        return self.render_to_response(self.get_context_data(form=form))


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


# class UserListView(LoginRequiredMixin, ListView):
#     """Контроллер списка пользователей"""
#     model = User
#     template_name = 'user_list.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    """Контроллер пользователя"""
    model = User


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     """Контроллер редактирования пользователя"""
#     model = User
#     fields = [
#         'id',
#         'phone',
#         'is_active',
#     ]
#     success_url = reverse_lazy('users:user_list')


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

        # Получаем пользователя по номеру телефона
        user = User.objects.filter(phone=phone).first()
        if not user:
            form.add_error('phone', 'Пользователь с таким номером не найден.')
            return self.form_invalid(form)

        # Генерация OTP и отправка SMS
        user.generate_otp()
        user.send_mock_sms()
        user.is_otp_sent = True
        user.save()

        messages.info(self.request, 'OTP отправлен на ваш номер телефона.')
        return redirect('users:otp_verify', pk=user.pk)


class PasswordResetVerifyView(FormView):
    """Подтверждение OTP и установка нового пароля"""
    template_name = 'users/otp_verify.html'
    form_class = OTPVerificationForm

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['user'] = user
        return context

    def form_valid(self, form):
        logger = logging.getLogger(__name__)
        logger.debug(f"Форма валидна, проверка OTP для пользователя {self.kwargs['pk']}")
        otp = form.cleaned_data['otp']
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # Проверяем OTP
        logger.debug(f"Проверка OTP для пользователя {user.pk}")
        if not user.verify_otp(otp):
            form.add_error('otp', 'Неверный код подтверждения.')
            return self.form_invalid(form)

        logger.debug(f"OTP для пользователя {user.pk} прошел проверку. Перенаправляем на страницу нового пароля.")

        # После успешной проверки OTP перенаправляем на страницу ввода нового пароля
        return redirect('users:new_password', pk=user.pk)


class NewPasswordView(FormView):
    """Контроллер ввода нового пароля"""
    template_name = 'users/new_password.html'
    form_class = NewPasswordForm

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
        return redirect('users:login')  # Перенаправление на страницу логина


class SubscribeView(TemplateView):
    """Контроллер подписки"""
    template_name = 'blog/subscribe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление подписки'
        return context


class CreatePaymentView(View):
    """Контроллер создания платежа для подписки"""

    def get(self, request, *args, **kwargs):
        price = create_stripe_price()
        session_id, session_url = create_stripe_session(price)
        payment = Payment.objects.create(
            user=request.user,
            amount=500,
            stripe_session_id=session_id,
            status='pending',
        )

        return redirect(session_url)

from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, FormView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.views import LoginView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from users.forms import UserRegisterForm, OTPVerificationForm, UserLoginForm, UserProfileForm
from users.models import User


class CreateUserView(CreateView):
    """Контроллер создания пользователя"""
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:otp_verify')

    def form_valid(self, form):
        """Генерируем OTP и отправляем SMS. Сохраняем пользователя."""
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user.generate_otp()
        user.send_mock_sms()
        messages.info(self.request, 'Введите OTP для подтверждения.')
        return HttpResponseRedirect(reverse_lazy('users:otp_verify') + f'?user_id={user.id}')


class UserOTPVerifyView(FormView):
    """Проверка OTP"""
    template_name = 'users/otp_verify.html'
    form_class = OTPVerificationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user_id = self.request.GET.get('user_id')
        user = get_object_or_404(User, id=user_id)
        otp = form.cleaned_data['otp']
        is_valid, message = user.verify_otp(otp)
        if is_valid:
            user.is_active = True
            user.save()
            messages.success(self.request, 'Подтверждение успешно!')
        else:
            messages.error(self.request, message)
        return HttpResponseRedirect(reverse_lazy('users:login'))


class UserLoginView(LoginView):
    """Контроллер логина"""
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True


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
    model = User
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('users:login')


class UserDeleteConfirmationView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'users/confirm_delete.html', {'user': user})

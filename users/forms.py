from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.forms import BooleanField
from phonenumber_field.formfields import PhoneNumberField

from users.models import User


class StyleFormMixin:
    """Миксин для стилизации формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форм для регистрации пользователя"""
    phone = PhoneNumberField(label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': '+71234567890'}))

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')

    def clean_password2(self):
        """Проверка, что пароли совпадают"""
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

    def clean_phone(self):
        """Проверка, что номер телефона еще не зарегистрирован"""
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким номером уже существует.')
        return phone

    def save(self, commit=True):
        """Генерируем OTP и отправляем SMS. Сохраняем пользователя."""
        user = super().save(commit=False)
        user.generate_otp()
        user.send_mock_sms()
        if commit:
            user.save()
        return user


class OTPVerificationForm(forms.Form):
    """Форма для ввода OTP"""
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        label='Код подтверждения',
        widget=forms.TextInput(attrs={'placeholder': 'Введите OTP'}),
    )


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма для авторизации пользователя"""

    class Meta:
        model = User
        fields = ('phone', 'password')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ('name', 'email', 'tg_nick', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

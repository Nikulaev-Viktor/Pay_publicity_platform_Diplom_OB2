from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.forms import BooleanField

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

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма для авторизации пользователя"""

    class Meta:
        model = User
        fields = ('phone', 'password')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ('name', 'email', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

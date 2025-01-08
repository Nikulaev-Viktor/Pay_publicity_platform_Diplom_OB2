import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """Проверка номера телефона"""
    pattern = r'^\+?[1-9]\d{1,14}$'  # Регулярное выражение для международных номеров
    if not re.match(pattern, value):
        raise ValidationError('Некорректный номер телефона. Убедитесь, что он введен в формате +71234567890.')

import random
from datetime import timedelta
from django.utils.timezone import now


def generate_otp():
    """Генерация случайного 6-значного кода"""
    return str(random.randint(100000, 999999))


def send_mock_sms(phone, otp_code):
    """Имитация отправки SMS"""
    if not phone:
        raise ValueError('Номер телефона отсутствует.')
    print(f'Отправлено SMS на {phone}: Ваш код подтверждения: {otp_code}')


def verify_otp(otp_code, otp_created_at, input_otp):
    """Проверка кода подтверждения."""
    if not otp_code:
        return False, 'Код подтверждения не был сгенерирован.'

    if otp_code != input_otp:
        return False, 'Неверный код подтверждения.'

    if otp_created_at and now() > otp_created_at + timedelta(minutes=5):
        return False, 'Срок действия кода истёк.'

    return True, 'Код подтвержден успешно.'

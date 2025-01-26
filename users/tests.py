from django.test import TestCase
from users.models import User, Payment
from django.utils.timezone import now
from unittest.mock import patch

from users.services import check_payment_status, create_stripe_session, create_stripe_price


class PaymentModelTests(TestCase):
    """Тесты для модели Payment."""

    def setUp(self):
        self.user = User.objects.create(phone='+71234567890', name='Test User', is_subscribed=False)
        self.payment = Payment.objects.create(
            user=self.user,
            amount=100.00,
            stripe_session_id='sess_123456',
            status='pending'
        )

    def test_payment_creation(self):
        """Тест на создание платежа."""
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.status, 'pending')
        self.assertIsNotNone(self.payment.created_at)

    def test_payment_status_update_and_subscription(self):
        """Тест обновления статуса платежа и активации подписки."""
        self.assertFalse(self.user.is_subscribed)
        self.payment.status = 'paid'
        self.payment.save()

        if self.payment.status == 'paid':
            self.user.is_subscribed = True
            self.user.save()

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_subscribed)
        self.assertEqual(self.payment.status, 'paid')

    def test_payment_str(self):
        """Тест строкового представления платежа."""
        self.assertEqual(str(self.payment),
                         f'Платеж {self.payment.id} - {self.payment.user} - {self.payment.amount} руб.')


class UserModelTests(TestCase):
    """Тесты для модели User."""

    def setUp(self):
        self.user = User.objects.create(
            phone='+71234567890',
            name='Test User',
            email='test@example.com',
            tg_nick='test_tg',
            avatar=None,
            is_subscribed=False
        )

    def test_user_creation(self):
        """Тест на создание пользователя."""
        self.assertEqual(self.user.phone, '+71234567890')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertFalse(self.user.is_subscribed)
        self.assertFalse(self.user.avatar)

    def test_user_str(self):
        """Тест строкового представления пользователя."""
        self.assertEqual(str(self.user), '+71234567890 - Test User')

    def test_nullable_fields(self):
        """Тест полей, которые могут быть пустыми или равными null."""
        self.user.email = None
        self.user.tg_nick = None
        self.user.save()
        self.user.refresh_from_db()
        self.assertIsNone(self.user.email)
        self.assertIsNone(self.user.tg_nick)

    @patch('users.models.generate_otp', return_value='123456')
    def test_generate_otp(self, mock_generate_otp):
        """Тест метода generate_otp."""
        self.user.generate_otp()
        self.assertEqual(self.user.otp_code, '123456')
        self.assertIsNotNone(self.user.otp_created_at)

    @patch('users.models.send_mock_sms')
    def test_send_mock_sms(self, mock_send_mock_sms):
        """Тест метода send_mock_sms."""
        self.user.otp_code = '123456'
        self.user.send_mock_sms()
        mock_send_mock_sms.assert_called_once_with(self.user.phone, '123456')

    @patch('users.models.verify_otp', return_value=(True, 'OTP verified successfully'))
    def test_verify_otp_success(self, mock_verify_otp):
        """Тест успешной проверки OTP."""
        self.user.otp_code = '123456'
        self.user.otp_created_at = now()
        self.user.save()
        is_valid, message = self.user.verify_otp('123456')
        self.assertTrue(is_valid)
        self.assertEqual(message, 'OTP verified successfully')
        self.assertIsNone(self.user.otp_code)

    @patch('users.models.verify_otp', return_value=(False, 'OTP is invalid or expired'))
    def test_verify_otp_failure(self, mock_verify_otp):
        """Тест неуспешной проверки OTP."""
        self.user.otp_code = '123456'
        self.user.otp_created_at = now()
        self.user.save()
        is_valid, message = self.user.verify_otp('654321')
        self.assertFalse(is_valid)
        self.assertEqual(message, 'OTP is invalid or expired')
        self.assertEqual(self.user.otp_code, '123456')

    def test_initial_subscription_status(self):
        """Проверка, что подписка изначально отключена."""
        self.assertFalse(self.user.is_subscribed)

    def test_subscription_status_after_payment(self):
        """Проверка, что подписка включается после успешной оплаты."""
        payment = Payment.objects.create(
            user=self.user,
            amount=500.00,
            stripe_session_id='test_session',
            status='paid'
        )
        if payment.status == 'paid':
            self.user.is_subscribed = True
            self.user.save()

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_subscribed)

    def test_subscription_status_not_changed_on_failed_payment(self):
        """Проверка, что подписка не включается после неуспешной оплаты."""
        payment = Payment.objects.create(
            user=self.user,
            amount=500.00,
            stripe_session_id='test_session',
            status='failed'
        )
        if payment.status == 'paid':
            self.user.is_subscribed = True
            self.user.save()

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_subscribed)


class StripeServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(phone="+71234567890", name="Test User")
        self.payment = Payment.objects.create(
            user=self.user,
            amount=500.00,
            stripe_session_id="test_session_id",
            status="pending"
        )

    @patch("users.services.stripe.Price.create")
    def test_create_stripe_price(self, mock_price_create):
        mock_price_create.return_value = {"id": "price_test_id", "currency": "rub"}
        price = create_stripe_price()
        self.assertEqual(price["id"], "price_test_id")
        self.assertEqual(price["currency"], "rub")
        mock_price_create.assert_called_once_with(
            currency="rub",
            unit_amount=50000,
            product_data={"name": "Subscription"},
        )

    @patch("users.services.stripe.checkout.Session.create")
    def test_create_stripe_session(self, mock_session_create):
        mock_session_create.return_value = {"id": "session_test_id", "url": "http://test_url"}
        session_id, session_url = create_stripe_session({"id": "price_test_id"})
        self.assertEqual(session_id, "session_test_id")
        self.assertEqual(session_url, "http://test_url")
        mock_session_create.assert_called_once_with(
            payment_method_types=["card"],
            line_items=[{"price": "price_test_id", "quantity": 1}],
            mode="payment",
            success_url="http://localhost:8000/users/subscribe/success/",
            cancel_url="http://localhost:8000/users/subscribe/cancel/",
        )

    @patch("users.services.stripe.checkout.Session.retrieve")
    def test_check_payment_status_paid(self, mock_session_retrieve):
        mock_session_retrieve.return_value = {"payment_status": "paid"}
        status = check_payment_status(self.user)
        self.payment.refresh_from_db()
        self.user.refresh_from_db()
        self.assertTrue(status)
        self.assertEqual(self.payment.status, "paid")
        self.assertTrue(self.user.is_subscribed)

    @patch("users.services.stripe.checkout.Session.retrieve")
    def test_check_payment_status_failed(self, mock_session_retrieve):
        mock_session_retrieve.return_value = {"payment_status": "failed"}
        status = check_payment_status(self.user)
        self.payment.refresh_from_db()
        self.assertFalse(status)
        self.assertEqual(self.payment.status, "failed")
        self.assertFalse(self.user.is_subscribed)

    @patch("users.services.stripe.checkout.Session.retrieve")
    def test_check_payment_status_pending(self, mock_session_retrieve):
        mock_session_retrieve.return_value = {"payment_status": "pending"}
        status = check_payment_status(self.user)
        self.payment.refresh_from_db()
        self.assertFalse(status)
        self.assertEqual(self.payment.status, "pending")
        self.assertFalse(self.user.is_subscribed)

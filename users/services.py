import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price():
    """Создаем стоимость в Stripe"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=50000,  # Стоимость подписки в копейках (500 рублей = 50000 копеек)
        product_data={"name": "Subscription"},
    )
    return price


def create_stripe_session(price):
    """Создаем сессию на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.get('id'),
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/users/subscribe/success/",
        cancel_url="http://localhost:8000/users/subscribe/cancel/",
    )
    return session.get('id'), session.get('url')


def check_payment_status(user):
    """Проверяем статус оплаты в Stripe"""
    session_id = user.payment_id
    if not session_id:
        return False

    session = stripe.checkout.Session.retrieve(session_id)
    payment_status = session.get("payment_status")

    if payment_status == "paid":
        user.is_subscribed = True
        user.save()
        return True
    elif payment_status == "failed":
        return False

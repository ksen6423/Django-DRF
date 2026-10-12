import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_stripe_price(amount):
    """Создает цену в страйпе."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        recurring={"interval": "month"},
        product_data={"name": "CoursePayment"},
    )

def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""
    sessions = stripe.checkout.Sessions.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return sessions.get("id"), sessions.get("url")
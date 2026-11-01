import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product.id


def create_stripe_price(product_id: str, amount: int) -> str:
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency="usd",
    )
    return price.id


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""
    sessions = stripe.checkout.Sessions.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return sessions.get("id"), sessions.get("url")

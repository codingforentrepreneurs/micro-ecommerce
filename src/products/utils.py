import stripe

from cfehome.env import config 

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY


def product_sales_pipeline(product_name="Test product", product_price=1000):
    stripe_product_obj = stripe.Product.create(name=product_name)
    stripe_product_id = stripe_product_obj.id
    stripe_price_obj = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=product_price,
        currency="usd"
    )
    stripe_price_id = stripe_price_obj.id
    base_endpoint = "http://127.0.0.1:8000"
    success_url = f"{base_endpoint}/purchases/success/"
    cancel_url = f"{base_endpoint}/purchases/stopped/"
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    print(checkout_session.url)
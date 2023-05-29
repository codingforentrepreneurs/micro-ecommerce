import stripe
from cfehome.env import config

# Obtener la clave secreta de Stripe desde la configuración del entorno
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)

# Establecer la clave secreta de Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Definir la función product_sales_pipeline
def product_sales_pipeline(product_name="Test product", product_price=1000):
    # Crear un objeto de producto en Stripe utilizando el nombre del producto proporcionado
    stripe_product_obj = stripe.Product.create(name=product_name)
    # Obtener el ID del producto creado
    stripe_product_id = stripe_product_obj.id

    # Crear un objeto de precio en Stripe utilizando el ID del producto y el precio del producto proporcionados
    stripe_price_obj = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=product_price,
        currency="usd"
    )
    # Obtener el ID del precio creado
    stripe_price_id = stripe_price_obj.id

    # Definir las URLs de éxito y cancelación para el flujo de pago
    base_endpoint = "http://127.0.0.1:8000"
    success_url = f"{base_endpoint}/purchases/success/"
    cancel_url = f"{base_endpoint}/purchases/stopped/"

    # Crear una sesión de pago de Stripe utilizando el ID del precio y otras opciones
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )

    # Imprimir la URL de la sesión de pago
    print(checkout_session.url)

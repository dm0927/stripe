import stripetest
from stripe_integration.config import StripeConfig


stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret


class Product:
    def __init__(self):
        pass

    def create(self, name):
        try:
            product = stripetest.Product.create(name=name, type='service')
            return product
        except Exception as e:
            print(f"Error creating product: {e}")
            return None

    def fetch(self, product_id):
        try:
            product = stripetest.Product.retrieve(product_id)
            return product
        except Exception as e:
            print(f"Error creating product: {e}")
            return None
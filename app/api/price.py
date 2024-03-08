import stripetest
from stripe_integration.config import StripeConfig


stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret


class Price:

    def __init__(self):
        pass

    def create(self, body):
        plan = {}
        try:
            if 'isrecurrent' in body and body['isrecurrent']:
                plan = stripetest.Price.create(
                    currency=body['currency'],
                    unit_amount=body['amount'],
                    recurring={"interval": body['interval']},
                    product_data={"name": body['product_name']},
                    nickname=body['nickname']
                )
            else:
                plan = stripetest.Price.create(
                    currency='usd',
                    unit_amount=body['amount'],
                    product_data={"name": body['product_name']}
                )
            return  {
                        'success' : True,
                        'data': plan
                    }
        except Exception as e:
            print(e)
            return  {
                        'success' : False,
                        'data': plan
                    }

    def fetch(self, price_id):
        try:
            price = stripetest.Price.retrieve(price_id)
            return price
        except Exception as e:
            print(f"Error creating product: {e}")
            return None
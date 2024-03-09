from api import Stripe

stripe = Stripe()

class PaymentIntent:

    def __init__(self):
        pass

    def create(self, stripe, body):
        try:
            paymentIntent = stripe.PaymentIntent.create(
                amount=body['amount'],
                currency=body['currency'],
                confirm=True,
                payment_method=body['payment_method'],
                automatic_payment_methods={
                    "enabled":True,
                    "allow_redirects":"never"
                }
            )
            return {   
                'status': True,
                'data': paymentIntent
            }
        except Exception as e:
            return {
                'status': False,
                'data': e
            }
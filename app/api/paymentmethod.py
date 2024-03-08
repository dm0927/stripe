import stripetest

from stripe_integration.config import StripeConfig


stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret


class PaymentMethod:

    def __init__(self):
        pass

    def attachPaymentMethod(self, body):
        try:

            # Atatch the payment method to the customer
            attachPaymentMethod = stripetest.PaymentMethod.attach(
                body['payment_method_id'],
                customer=body['customer_id'],
            )

            return {
                'success' : True,
                'data' : attachPaymentMethod
            }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }
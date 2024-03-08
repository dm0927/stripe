import json
import stripetest
from stripe_integration.api.customer import Customer
from stripe_integration.api.paymentmethod import PaymentMethod
from stripe_integration.api.invoice import Invoice
from stripe_integration.config import StripeConfig

stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret


class TopUp:

    def __init__(self):
        self.paymentMethod = PaymentMethod()
        self.customer = Customer()

    def create(self,body):

        try:
            # have to check invoice for this, create invoice with charge automatically

            top_up_info = stripetest.PaymentIntent.create(
                                                amount=body["amount"],
                                                currency=body["currency"],
                                                automatic_payment_methods={"enabled": True,"allow_redirects":"never"},
                                                customer=body["customer_id"],
                                                payment_method=body["payment_method_id"],
                                                transfer_data={"destination": body["brand_stripe_account"]}, #we can add amount here to transfer only that amount to brand account
                                                confirm=True
                                                )

            return {
                'success': True,
                'data': top_up_info
            }
        except Exception as e:
            return {
                'success': False,
                'data': e
            }



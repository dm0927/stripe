import json
import stripetest

from stripe_integration.config import StripeConfig


stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret


class Customer:

    def __init__(self):
        pass

    def create(self, body):
        try:
            
            customer = stripetest.Customer.create(
                name=body['customer_name'],
                email=body['customer_email'],
                metadata={"data": json.dumps(body['customer_metadata'])}
            )
            return customer

        except Exception as e:
            print("customer create exception: ", e)
            return {}

    def defaultAttachPaymentMethod(self, body):
        try:
            customer = stripetest.Customer.modify(
                body['customer_id'],
                invoice_settings = {
                    'default_payment_method' : body['payment_method_id']
                }   
            )

            return {
                'success' : True,
                'data' : customer
            }
        except Exception as e:
            print("defaultAttachPaymentMethod: ", e)
            return {
                'success' : False,
                'data' : e
            }
    
    def retrieve(self, customer_id):
        try:
            customer = stripetest.Customer.retrieve(customer_id)
            return {
                'success' : True,
                'data' : customer
            }
        except Exception as e:
            print("customer retrieve: ", e)
            return {
                'success' : False,
                'data' : e
            }

    def search(self, query):
        try:
            customer = stripetest.Customer.search(query=query)
            return customer

        except Exception as e:
            print("customer search exception: ", e)
            return {}
    
    def cancel(self, customer_id):
        try:
            customer = stripetest.Customer.delete(customer_id)
            return {
                'success' : True,
                'data' : customer
            }
        except Exception as e:
            print("customer cancel: ", e)
            return {
                'success' : False,
                'data' : e
            }
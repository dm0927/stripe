import stripetest

from stripe_integration.config import StripeConfig
stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret

class Card:
    def createCardToken(self, body):
        try:

            token_details = stripetest.Token.create(
                card={
                    "number": body["number"],
                    "exp_month": body["exp_month"],
                    "exp_year": body["exp_year"],
                    "cvc": body["cvc"],
                },
            )

            return {
                'success': True,
                'data': token_details
            }
        except Exception as e:
            return {
                'success': False,
                'data': e
            }

        pass


    def retrive_token(self, body):
        try:
            token_details = stripetest.Token.retrieve(body['tokenId'])

            return {
                'success': True,
                'data': token_details
            }
        except Exception as e:
            return {
                'success': False,
                'data': e
            }

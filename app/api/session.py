class Session:

    def createSubscriptionSession(self, stripe, body):
        try:
            # Create a new subscription session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': body['priceId'],
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=body['successUrl'],
                cancel_url=body['cancelUrl'],
                customer=body['customer_id'],
                allow_promotion_codes=body['allow_promotion_codes']
            )
            return session
        except Exception as e:
            return str(e)
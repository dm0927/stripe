from run import app
import stripe

class Stripe:
    def __init__(self):
        stripe.api_key = app.config['STRIPE_SECRET_KEY']
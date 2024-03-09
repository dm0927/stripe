from flask import Blueprint
from app.controllers.paymentintent import PaymentPage

paymentintent = Blueprint('paymentintent', __name__)

paymentintent.add_url_rule('/payment-page', view_func=PaymentPage.as_view('payment_page'))


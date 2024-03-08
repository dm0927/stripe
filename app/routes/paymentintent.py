from flask import Blueprint, jsonify, make_response, request, render_template

paymentintent = Blueprint('paymentintent', __name__)

@paymentintent.route('/payment-page', methods=['GET'])
def payment_page():
    return render_template('payment-page.html')

@paymentintent.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = {
        'name': 'T-shirt',
    }

    response = make_response(jsonify(data), 200)
    return response
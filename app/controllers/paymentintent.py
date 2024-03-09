from flask import jsonify, make_response, request, render_template
from flask.views import MethodView
# from api.paymentintent


class PaymentPage(MethodView):
    def get(self):
        return render_template('payment-page.html')

# @paymentintent.route('/create-payment-intent', methods=['POST'])
# def create_payment():

#     data = request.json
    

#     response = make_response(jsonify(data), 200)
#     return response
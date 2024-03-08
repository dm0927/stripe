class Coupon:
    def __init__(self):
        pass

    def create(self, stripe, body):
        print(body)
        try:
            if 'amount_off' in body and 'currency' in body:
                '''
                    If a direct discount of a specific amount is to given to the customer we use the amount_off and currency, as currency is required for amount_off
                    amount_off: The amount that will be taken off the subtotal of any invoices for this customer.
                    currency: Three-letter ISO currency code, in lowercase. Must be a supported currency.
                    max_redemptions: A positive integer specifying the number of times the coupon can be redeemed before it’s no longer valid.
                '''
                coupon = stripe.Coupon.create(
                    amount_off=body['amount_off'],
                    # duration=body['duration'],
                    currency=body['currency'],
                    max_redemptions=body['max_redemptions'] if body['max_redemptions'] > 0 else 1,
                    redeem_by=body['expires_at'] if 'expires_at' in body else None, 
                )
            else:
                coupon = stripe.Coupon.create(
                    percent_off=body['percent_off'],
                    # duration=body['duration'],
                    max_redemptions=body['max_redemptions'],
                    redeem_by=body['expires_at'] if 'expires_at' in body else None,
                )
            return {
                'success': True,
                'data': coupon
            }
        except Exception as e:  
            return {
                'success': False,
                'data': e
            }
    
    def subscriptionCoupon(self, stripe, body):
        try:
            '''
                If a direct discount of a specific amount is to given to the customer we use the amount_off and currency, as currency is required for amount_off
                amount_off: The amount that will be taken off the subtotal of any invoices for this customer.
                currency: Three-letter ISO currency code, in lowercase. Must be a supported currency.
                duration: Specifies how long the discount will be in effect. Can be forever, once, or repeating. Applies on the subscription level.
                duration_in_months: If duration is repeating, a positive integer that specifies the number of months the discount will be in effect.
                name: Name of the coupon to be displayed on the dashboard. If not provided, will be the same as the id.
                max_redemptions: A positive integer specifying the number of times the coupon can be redeemed before it’s no longer valid.
                redeem_by: Unix timestamp specifying the last time at which the coupon can be redeemed. After the redeem_by date, the coupon can no longer be applied to new customers.
            '''
            coupon = stripe.Coupon.create(
                amount_off=body['amount_off'],
                currency=body['currency'],
                duration=body['duration'] if 'duration' in body else 'once',
                duration_in_months = 1 if body['duration'] == "repeating" else 0,
                # metadata = {}
                name = body['name'] if 'name' in body else None,
                max_redemptions=body['max_redemptions'],
                redeem_by = body['redeem_by'] if 'redeem_by' in body else None,

            )
            return {
                'success': True,
                'data': coupon
            }
        except Exception as e:  
            return {
                'success': False,
                'data': e
            }
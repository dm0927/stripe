from api.coupon import Coupon

class PromotionCode:
    def __init__(self) -> None:
        pass
    
    def create(self, stripe, body):
        try:

            '''
                coupon_id: The ID of the coupon that the promotion code can be redeemed with. Required Field
                customer_id: The customer that can redeem the promotion code. Required Field
                code: The customer-facing code that can be redeemed with the coupon.
                expires_at: The timestamp at which this promotion code will expire. If the coupon has specified a redeems_by, then this value cannot be after the coupon’s redeems_by.
            '''
            data = Coupon().create(stripe, body)

            if data['success']:

                body['coupon_id'] = data['data']['id']
            else:
                return {
                    'success': False,
                    'data': "Unable to create promotion code as coupon creation failed."
                }

            promotion_code = stripe.PromotionCode.create(
                coupon=body['coupon_id'],
                customer=body['customer_id'],
                code=body['code'] if 'code' in body else '',
                expires_at=body['expires_at'] if 'expires_at' in body else None,

            )
            return {
                'success': True,
                'data': promotion_code
            }
        except Exception as e:
            return {
                'success': False,
                'data': e
            }
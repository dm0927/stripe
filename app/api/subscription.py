import json
import stripetest
from stripe_integration.api.customer import Customer
from stripe_integration.api.paymentmethod import PaymentMethod
from stripe_integration.api.price import Price
from stripe_integration.api.invoice import Invoice
from stripe_integration.api.coupon import Coupon
from stripe_integration.config import StripeConfig


stripetest.api_key = StripeConfig.API_KEY
endpoint_secret = StripeConfig.endpoint_secret


class Subscription:

    def __init__(self):
        self.paymentMethod = PaymentMethod()
        self.customer = Customer()

    def create(self, body):
        try:

            body['trial'] = body['trial'] if 'trial' in body and body['trial'] > 0 else 0
            
            self.paymentMethod.attachPaymentMethod(body)
            self.customer.defaultAttachPaymentMethod(body)

            getCustomer = self.customer.retrieve(body['customer_id'])
            if getCustomer['success']:
                default_payment_method_id = getCustomer['data'].invoice_settings.default_payment_method
                subscription = stripetest.Subscription.create(
                    customer=body['customer_id'],
                    items=[
                        {
                            'price': body['price_id'],
                        },
                    ],
                    default_payment_method=default_payment_method_id,
                    trial_period_days = body['trial'], # This is the trial period for the subscription this needs to be altered as we don't get payment intent
                    coupon = body['coupon_id'],
                )
                return {
                    'success' : True,
                    'data' : subscription
                }
            else:
                return {
                    'success' : False,
                    'data' : "Wasn't able to retrieve the customer"
                }
        except Exception as e:
            print("subcreate: ", e)
            return {
                'success' : False,
                'data' : e
            }
    
    def cancel(self, body):
        try:
            subscription = stripetest.Subscription.cancel(body['subscription_id'])
            return {
                        'success' : True,
                        'data' : subscription
                    }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }
    
    def retrieve(self, stripe, subscription_id):
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'success' : True,
                'data' : subscription
            }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }
    
    def upgrade(self, stripe, body):
        try:

            subscription = self.retrieve(stripe, body['subscription_id'])

            if subscription['success']:
                subscription = subscription['data']

                subscription = stripe.Subscription.modify(
                    body['subscription_id'],
                    cancel_at_period_end=False,
                    items=[
                        {
                            'id': subscription['items']['data'][0].id,
                            'price': body['price_id'],
                        },
                    ],
                    expand=['latest_invoice.payment_intent'],
                    proration_behavior = "always_invoice",          # It will generate the invoice for the remaining amount
                )
                return {
                    'success' : True,
                    'data' : subscription
                }
            else:
                return {
                    'success' : False,
                    'data' : "Wasn't able to retrieve the subscription"
                }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }

    def customCreate(self, stripe, body):
        price = Price().create(stripe, body)

        if price['success']:
            price = price['data']

            customer = Customer().create(stripe, body)

            if customer['success']:
                customer = customer['data']

                couponId = None
                '''
                    A coupoun to be applied dynamically on the subscription, the invoice will be generated with the coupon applied, as I haven't found a way to apply 
                    the coupon on the invoice by the customer.
                '''
                if 'amount_off' in body and body['amount_off'] != '':
                    coupon = Coupon().subscriptionCoupon(stripe, body)   
                    if coupon['success']:
                        couponId = coupon['data'].id
                
                try:
                    subscription = stripe.Subscription.create(
                                    customer=customer.id,
                                    items=[
                                        {
                                            'price': price.id,
                                        },
                                    ],
                                    payment_behavior='allow_incomplete',
                                    collection_method='send_invoice',
                                    days_until_due=1,
                                    payment_settings={"payment_method_types": ['card']},
                                    coupon=couponId,
                                    metadata={'data':json.dumps(body['metadata'])}
                                ) 
                    
                    Invoice().list(stripe, customer.id, subscription.id)

                    return {
                        'success' : True,
                        'data' : subscription
                    }
                except Exception as e:
                    return {
                        'success' : False,
                        'data' : e
                    }
            else:
                return {
                    'success' : False,
                    'data' : "Stripe was unable to create the customer"
                }
        else:
            return {
                'success' : False,
                'data' : "Stripe was unable to create the price"
            }
    
    def modify(self, stripe, subscription_id, cancelAtPeriodEnd=False):
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=cancelAtPeriodEnd,
            )
            return {
                'success' : True,
                'data' : subscription
            }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }
    
    def createScheduleSubscriptionStart(self, stripe, scheduleSubscriptionStart, customerId, price_id):
        try:
            subscriptionSchedule = stripe.SubscriptionSchedule.create(
                customer=customerId,
                start_date=scheduleSubscriptionStart,
                end_behavior='release',
                phases=[
                    {
                        'items': [
                            {
                                'price': price_id,
                            }
                        ]
                    },
                ],
            )
            return {
                'success' : True,
                'data' : subscriptionSchedule
            }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }

    def downgrade(self, stripe, body):
        try:
            subscription = self.retrieve(stripe, body['subscription_id'])

            if subscription['success']:

                #Cancel the subscription at the period end
                response = self.modify(stripe, body['subscription_id'], True)
                if response['success']:
                    subscription = subscription['data']
                    scheduleSubscriptionStart = subscription['current_period_end']
                    customerId =  subscription['customer']

                    subscriptionSchedule = self.createScheduleSubscriptionStart(stripe, scheduleSubscriptionStart, customerId, body['price_id'])

                    return subscriptionSchedule
                else:
                    return {
                        'success' : False,
                        'data' : "Modification of the subscription failed"
                    }    
            else:
                return {
                    'success' : False,
                    'data' : "Wasn't able to retrieve the subscription"
                }
        except Exception as e:
            return {
                'success' : False,
                'data' : e
            }
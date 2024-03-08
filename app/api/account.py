from api.paymentintent import PaymentIntent
class Account:

    def __init__(self):
        pass

    def create(self, stripe):
        try:
            accountDetails = stripe.Account.create(
                                    type="custom",
                                    business_type="individual",
                                    capabilities={
                                        "card_payments": {"requested": True},
                                        "transfers": {"requested": True},
                                    },
                                    tos_acceptance={
                                        "date": 1610518260,
                                        "ip": "8.8.8.8",
                                        "service_agreement": "full",
                                        "user_agent": "Mozilla/5.0",
                                    },
                                    company={
                                        "name": "Jenny Rosen",
                                        "tax_id":  "000000000",
                                    },
                                    individual={
                                        "first_name": "Jenny",
                                        "last_name": "Rosen",
                                        "email": "dm2709@mailinator.com",
                                        "phone": "+17746882268",
                                        "address": {
                                                "line1": "address_full_match",
                                                "city": "San Francisco",
                                                "state": "CA",
                                                "country": "US",
                                                "postal_code": "94103",
                                            },
                                        "id_number": "000000000",
                                        "ssn_last_4": "0000",
                                        "dob": {    
                                            "day": 1,
                                            "month": 1,
                                            "year": 1901,
                                        },
                                    },
                                    business_profile={
                                        'mcc':  5734,   
                                        "url": "https://www.abcd.com",
                                    },
                                    country="US",
                                    email="jenny.rosen@example.com",
                                )
            return {
                "status": "success",
                "data": accountDetails
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def topup(self, stripe, body):
        paymentIntent = PaymentIntent().create(stripe, body)
        if paymentIntent['status']:
            try:
                topupDetails = stripe.Topup.create(
                    amount=body['amount'],
                    currency="usd",
                    description="Top-up for account",
                    statement_descriptor="Top-up",
                    source="btok_us_verified",
                )
                return {
                    "status": True,
                    "data": topupDetails
                }
            except Exception as e:
                return {
                    "status": False,
                    "message": str(e)
                }
        else:
            return {
                "status": True,
                "message" : ""
            }
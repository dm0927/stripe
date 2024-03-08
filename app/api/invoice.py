class Invoice:
    def __init__(self):
        pass

    def list(self, stripe, customer, subscription):
        try:
            invoice = stripe.Invoice.list(customer=customer.id, subscription=subscription.id, limit=1).data[0]
            invoiceSend = self.sendInvoice(stripe, invoice.id)
            return {    
                'success' : True,
                'data' : invoiceSend
            }
        except:
            return {
                'success': False,
                'data': 'Error getting invoice'
            }

    def sendInvoice(self, stripe, invoiceId):
        try:
            invoiceSend = stripe.Invoice.send_invoice(invoiceId)
            return {
                'success': True,
                'data' : invoiceSend
            }
        except:
            return {
                'success': False,
                'data': 'Error sending invoice'
            }
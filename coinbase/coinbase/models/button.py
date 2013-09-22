from amount import CoinbaseAmount
from contact import CoinbaseContact

class CoinbaseButton(object):

    def __init__(self, button):
        #"code": "93865b9cae83706ae59220c013bc0afd",
        #"type": "buy_now",
        #"style": "custom_large",
        #"text": "Pay With Bitcoin",
        #"name": "test",
        #"description": "Sample description",
        #"custom": "Order123",
        #"callback_url": "http://www.example.com/my_custom_button_callback",
        #"price": {
        #    "cents": 123,
        #    "currency_iso": "USD"
        #}

        self.code = button['code']
        self.custom = button['custom']
        #self.notes = transaction['notes']

        #transaction_amount = transaction['amount']['amount']
        #transaction_currency = transaction['amount']['currency']

        #self.amount = CoinbaseAmount(transaction_amount, transaction_currency)

        #self.status = transaction['status']
        #self.request = transaction['request']


        ##Sender Information
        #if 'sender' in transaction:
        #    sender_id = transaction['sender'].get('id', None)
        #    sender_name = transaction['sender'].get('name', None)
        #    sender_email = transaction['sender'].get('email', None)

        #    self.sender = CoinbaseContact(contact_id=sender_id,
        #                                  name=sender_name,
        #                                  email=sender_email)

        #else:
        #    #TODO:  Not sure what key would go here
        #    pass

        ##Recipient Info
        #if 'recipient' in transaction:
        #    recipient_id = transaction['recipient'].get('id', None)
        #    recipient_name = transaction['recipient'].get('name', None)
        #    recipient_email = transaction['recipient'].get('email', None)

        #    self.recipient = CoinbaseContact(contact_id=recipient_id,
        #                                  name=recipient_name,
        #                                  email=recipient_email)
        #    self.recipient_address = None
        #    self.recipient_type = 'CoinBase'

        #elif 'recipient_address' in transaction:
        #    self.recipient = None
        #    self.recipient_address = transaction['recipient_address']
        #    self.recipient_type = 'Bitcoin'

    def refresh(self):
        pass
        #TODO:  Refresh the transaction

    def cancel(self):
        pass
        #TODO:  Cancel the transaction if possible

    def complete(self):
        pass
        #TODO:  Approve the transaction if possible

    def resend(self):
        pass
        #TODO:  Resend the transaction email if possible

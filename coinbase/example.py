__author__ = 'gsibble'

from coinbase import CoinbaseAccount
import oauth2client

#Use oAuth2client web flow to get JSON credentials (see coinbase_oauth2 example)
TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-03-31T22:48:20Z", "access_token": "c15a9f84e471db9b0b8fb94f3cb83f08867b4e00cb823f49ead771e928af5c79", "token_uri": "https://www.coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "c15a9f84e471db9b0b8fb94f3cb83f08867b4e00cb823f49ead771e928af5c79", "token_type": "bearer", "expires_in": 7200, "refresh_token": "90cb2424ddc39f6668da41a7b46dfd5a729ac9030e19e05fd95bb1880ad07e65", "scope": "all"}, "client_id": "2df06cb383f4ffffac20e257244708c78a1150d128f37d420f11fdc069a914fc", "id_token": null, "client_secret": "7caedd79052d7e29aa0f2700980247e499ce85381e70e4a44de0c08f25bded8a", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "90cb2424ddc39f6668da41a7b46dfd5a729ac9030e19e05fd95bb1880ad07e65", "user_agent": null}'''

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-09-22T19:56:46Z", "access_token": "b0ae06f3f1f165b6eba0f19849a82028b1085c6dc731e1e349e805def363340a", "token_uri": "https://coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "b0ae06f3f1f165b6eba0f19849a82028b1085c6dc731e1e349e805def363340a", "token_type": "bearer", "expires_in": 7200, "refresh_token": "75151e031d3f5ff4b159bd559fb65776e8ea32fae68b82589e14256b601fcfc7", "scope": "all"}, "client_id": "1e6dc802a76840817a9055a49dc86ae801ad4b474d5a97a1b7dce1e3cc01b1bc", "id_token": null, "client_secret": "00579619f736854a922e18d2652e6608cad3f83abe0d8e3327b3c588905314e1", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "75151e031d3f5ff4b159bd559fb65776e8ea32fae68b82589e14256b601fcfc7", "user_agent": null}'''


def do_coinbase_stuff(account):
    print 'The current value of 1 BTC in USD is: $' + str(account.sell_price())
    print 'The current value of 10 BTC in USD is: $' + str(account.sell_price(qty=10))
    print 'You can buy 1 bitcoin for ' + str(account.buy_price()) + ' USD'
    print 'Your balance is ' + str(account.balance) + ' BTC'
    print 'That means your account value in USD is $' + str(account.sell_price(qty=account.balance))

    print 'Your receive address is ' + str(account.receive_address)
    print 'You have the following people in your address book:'
    print [contact['email'] for contact in account.contacts]

    print 'Would you like to try moving some Bitcoin around?'
    response = raw_input("Type YES if so: ")

    if response == 'YES':
        print "Awesome!  Let's do it.  First, let's have you make a request to someone for some BTC."
        request_btc_from_email = raw_input("What email address would you like to request BTC from: ")
        amount_to_request = raw_input("How much BTC would you like to request: ")
        print 'Setting up request to ' + request_btc_from_email
        request_transaction = account.request(from_email=request_btc_from_email,
                                              amount=amount_to_request,
                                              notes='Test request')
        print "We successfully created a request for " + request_transaction.sender.email + " to send you " + str(
            request_transaction.amount) + " " + request_transaction.amount.currency

        print "Now would you like to send some bitcoin? Plese note this will really send BTC from your account."
        send_response = raw_input("Type YES if so: ")

        if send_response == 'YES':
            print "Awesome!  Let's do that!"
            send_btc_to = raw_input("Please enter a Bitcoin address to send money to: ")
            amount_to_send = raw_input("How much BTC would you like to send: ")
            send_transaction = account.send(to_address=send_btc_to,
                                            amount=amount_to_send,
                                            notes='Test send')

            print "We successfully sent " + str(
                send_transaction.amount) + " " + send_transaction.amount.currency + " to " + send_transaction.recipient_address

            print "Your new balance is " + str(account.balance)

    transactions = account.transactions(count=30)

    print "Here are your last " + str(len(transactions)) + " transactions:"

    for index, transaction in enumerate(transactions):

        if transaction.amount > 0:
            print str(index) + ": " + str(transaction.amount) + " " + transaction.amount.currency + " to your Coinbase wallet."
        else:
            print str(index) + ": " + str(transaction.amount) + " " + transaction.amount.currency + " out to a " + transaction.recipient_type + " address"


if __name__ == '__main__':
    account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    do_coinbase_stuff(account=account)

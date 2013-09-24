import oauth2client

from coinbase import CoinbaseAccount
from coinbase import TEMP_CREDENTIALS
from coinbase import API_KEY

#account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
account = CoinbaseAccount(api_key=API_KEY)

def get_rates():
    #account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    global account

    rates = {}
    rates['buy'] = float(account.buy_price())
    rates['sell'] = float(account.sell_price())
    print rates
    return rates

def create_invoice(data):
    #account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    global account
        
    button = account.create_button(data)
    print data
    print 'https://coinbase.com/checkouts/%s?c=a' % button.code
    return button.code

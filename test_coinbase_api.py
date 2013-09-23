import oauth2client

from coinbase import CoinbaseAccount
from coinbase import TEMP_CREDENTIALS
from coinbase import API_KEY


def test_get_rates(account):
    print 'Sell: %s USD' % account.sell_price()
    print 'Buy: %s USD' % account.buy_price()

def test_create_invoice(account):
    data = {
        "name": "test",
        "price_string": "1.23",
        "price_currency_iso": "USD",
        "custom": "Order123",
        "callback_url": "http://www.example.com/my_custom_button_callback",
        "description": "Sample description",
        "type": "buy_now",
        "style": "custom_large"
    }
        
    button = account.create_button(data)
    print 'https://coinbase.com/checkouts/%s?c=a' % button.code
    return button.code

if __name__ == '__main__':
    #account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    account = CoinbaseAccount(api_key=API_KEY)
    test_get_rates(account=account)
    test_create_invoice(account=account)

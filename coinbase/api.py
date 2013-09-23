import oauth2client

from coinbase import CoinbaseAccount

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-09-22T20:34:54Z", "access_token": "b0ae06f3f1f165b6eba0f19849a82028b1085c6dc731e1e349e805def363340a", "token_uri": "https://coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "b0ae06f3f1f165b6eba0f19849a82028b1085c6dc731e1e349e805def363340a", "token_type": "bearer", "expires_in": 7200, "refresh_token": "75151e031d3f5ff4b159bd559fb65776e8ea32fae68b82589e14256b601fcfc7", "scope": "all"}, "client_id": "1e6dc802a76840817a9055a49dc86ae801ad4b474d5a97a1b7dce1e3cc01b1bc", "id_token": null, "client_secret": "00579619f736854a922e18d2652e6608cad3f83abe0d8e3327b3c588905314e1", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "75151e031d3f5ff4b159bd559fb65776e8ea32fae68b82589e14256b601fcfc7", "user_agent": null}'''

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-09-22T22:20:51Z", "access_token": "68dc9ae0a3a160411fe3a92319cfee474865229ea2c8edeb4241a81140be9146", "token_uri": "https://coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "68dc9ae0a3a160411fe3a92319cfee474865229ea2c8edeb4241a81140be9146", "token_type": "bearer", "expires_in": 7200, "refresh_token": "ac4aad355b339a26649b76a1b80d3c4f8469b8f8f8ded0f99882002d3b76d5b8", "scope": "all"}, "client_id": "1e6dc802a76840817a9055a49dc86ae801ad4b474d5a97a1b7dce1e3cc01b1bc", "id_token": null, "client_secret": "00579619f736854a922e18d2652e6608cad3f83abe0d8e3327b3c588905314e1", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "ac4aad355b339a26649b76a1b80d3c4f8469b8f8f8ded0f99882002d3b76d5b8", "user_agent": null}'''

TEMP_CREDENTIALS = '''{"_module": "oauth2client.client", "token_expiry": "2013-09-22T22:20:51Z", "access_token": "68dc9ae0a3a160411fe3a92319cfee474865229ea2c8edeb4241a81140be9146", "token_uri": "https://coinbase.com/oauth/token", "invalid": false, "token_response": {"access_token": "68dc9ae0a3a160411fe3a92319cfee474865229ea2c8edeb4241a81140be9146", "token_type": "bearer", "expires_in": 7200, "refresh_token": "ac4aad355b339a26649b76a1b80d3c4f8469b8f8f8ded0f99882002d3b76d5b8", "scope": "all"}, "client_id": "1e6dc802a76840817a9055a49dc86ae801ad4b474d5a97a1b7dce1e3cc01b1bc", "id_token": null, "client_secret": "00579619f736854a922e18d2652e6608cad3f83abe0d8e3327b3c588905314e1", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "ac4aad355b339a26649b76a1b80d3c4f8469b8f8f8ded0f99882002d3b76d5b8", "user_agent": null}'''

account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)

def get_rates():
    #account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    global account
    print 'Sell: %s USD' % account.sell_price()
    print 'Buy: %s USD' % account.buy_price()
    rates = {}
    rates['buy'] = float(account.buy_price())
    rates['sell'] = float(account.sell_price())
    return rates

def create_invoice(data):
    #account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    global account
    #data = {
    #    "name": "test",
    #    "price_string": "1.23",
    #    "price_currency_iso": "USD",
    #    "custom": "Order123",
    #    "callback_url": "http://www.example.com/my_custom_button_callback",
    #    "description": "Sample description",
    #    "type": "buy_now",
    #    "style": "custom_large"
    #}
        
    button = account.create_button(data)
    print 'https://coinbase.com/checkouts/%s?c=a' % button.code
    return button.code

def test_get_rates(account):
    print 'Sell: %s USD' % account.sell_price()
    print 'Buy: %s USD' % account.buy_price()

def test_create_invoice(account):
    print 'Sell: %s USD' % account.sell_price()
    print 'Buy: %s USD' % account.buy_price()
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
    account = CoinbaseAccount(oauth2_credentials=TEMP_CREDENTIALS)
    test_get_rates(account=account)
    test_create_invoice(account=account)

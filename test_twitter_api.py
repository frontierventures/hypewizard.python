import twitter_api

if __name__ == '__main__':
    #account = CoinbaseAccount(api_key=API_KEY)
    #test_get_rates(account=account)
    #test_create_invoice(account=account)
    print twitter_api.get_followers_count('coingig')

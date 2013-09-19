import twitter
import json

api = twitter.Api()

api = twitter.Api(consumer_key='PZbYciNC8TS3LVxeHaBTg',
                  consumer_secret='o4sKqGuCkuVnlTTiYe4FcHC82UtGprdZVGqjyMGz18',
                  access_token_key='632058592-trS5QTBYedptP4AFik4w1mwFcId74EK5qBy1VbHE',
                  access_token_secret='SUIZajSIznRzvPWNKUgkGPZnLlyXLTYq5YvLZVGrq4M')

def get_followers_count(twitter_name):
    user = api.GetUser(screen_name=twitter_name)
    return user.followers_count

def get_statuses(twitter_name):
    # user = api.GetUser(screen_name="coingig")
    statuses = []
    if twitter_name:
        statuses = api.GetUserTimeline(screen_name=twitter_name)
    return statuses

def get_user(twitter_name):
    user = api.GetUser(screen_name=twitter_name)
    return user

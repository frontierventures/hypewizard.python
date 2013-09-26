import json
import time, datetime
import twitter
import config

api = twitter.Api()

api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                  consumer_secret=config.CONSUMER_SECRET,
                  access_token_key=config.ACCESS_TOKEN,
                  access_token_secret=config.ACCESS_TOKEN_SECRET)

def get_followers_count(twitter_name):
    user = api.GetUser(screen_name=twitter_name)
    return user.followers_count

def get_user_by_id(twitter_id):
    user = api.GetUser(user_id=twitter_id)
    return user

def convert_twitter_timestamp(created_at):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
    return timestamp

def get_status(status_id):
    status = api.GetStatus(status_id, trim_user=True, include_my_retweet=True, include_entities=True)
    return status

#def get_retweets(status_id):
#    statuses = api.GetRetweets(status_id, count=100, trim_user=False) 
#    return statuses

#####################################
# Usefull
#####################################

def get_statuses(twitter_id):
    # user = api.GetUser(screen_name="coingig")
    statuses = []
    statuses = api.GetUserTimeline(user_id=twitter_id, include_rts=False, exclude_replies=True)
    return statuses

# Used for first login
def get_user(twitter_name=None, twitter_id=None):
    response = {
        'error': False
    }
    try:
        user = api.GetUser(screen_name=twitter_name, user_id=twitter_id)
        response['user'] = user
    except twitter.TwitterError, error:
        response['error'] = True
        response['message'] = error[0][0]['message']
        #print error
    return response

def get_retweets(status_id):
    response = {
        'error': False
    }
    try:
        retweets = api.GetRetweets(status_id, count=100, trim_user=False) 
        response['retweets'] = retweets
    except twitter.TwitterError, error:
        response['error'] = True
        response['message'] = error[0][0]['message']
        #print error
    return response

def verify_transaction(promoter_id, status_id):
    response = twitter_api.get_retweets(status_id)
    for retweet in response['retweets']:
        print retweet
        print retweet.user.id

        if str(retweet.user.id) == str(promoter_id):
            print retweet.created_at, retweet.user.screen_name
            print "Match"
            #twitter_api.convert_twitter_timestamp(tweet.retweeted_status.created_at), 
        print

def get_retweet_duration(promoter_id, status_id):
    print "promoter_id: %s" % promoter_id
    print "status_id: %s" % status_id
    response = {
        'error': False
    }
    response = get_retweets(status_id)
    retweets = response['retweets']

    is_retweet_found = False
    delta = 0
    for retweet in retweets:
        print retweet.user.id, retweet.user.screen_name, retweet.created_at

        if str(retweet.user.id) == str(promoter_id):
            dt1 = parse(retweet.created_at)
            dt1 = dt1.replace(tzinfo=None)
            seconds1 = (dt1 - datetime(1970,1,1)).total_seconds()
    
            dt2 = datetime.utcnow() #current utc time 
            seconds2 = (dt2 - datetime(1970,1,1)).total_seconds()
    
            delta = seconds2 - seconds1
            is_retweet_found = True

    response = {}
    response['is_retweet_found'] = is_retweet_found
    response['error'] = False
    response['delta'] = delta
    return response
    
#####################################
# Usefull
#####################################


# User for maturity calculation
#def get_timeline(twitter_id):
#    response = {
#        'error': False
#    }
#    try:
#        timeline = api.GetUserTimeline(user_id=twitter_id)
#        response['timeline'] = timeline
#    except twitter.TwitterError, error:
#        response['error'] = True
#        response['message'] = error[0][0]['message']
#        #print error
#    return response
    #account = CoinbaseAccount(api_key=API_KEY)
    #test_get_rates(account=account)
    #test_create_invoice(account=account)
    #print twitter_api.get_followers_count('coingig')

status_id = '380866222369144832' # Client Status Id 
screen_name = 'hypewizard'

#from datetime import datetime, date, time
from dateutil.parser import parse
from datetime import datetime

#is_promotional_period_over(status_id, screen_name)

        
#dt = parse("Tue, 22 Jul 2008 08:17:41 +0200")
#print -time.timezone # Local timezone

# convert twitter time to datetime
# apply offset
# find the difference
#print time.strftime('%Y-%m-%d %H:%M:%S', current_timestamp) 
# find if promoter posted

#statuses = get_statuses('hypewizard')
#for status in statuses:

# find post timestamp
# find time difference between now and the post time
# figure out timezones


#print get_status(status_id)
#
#statuses = get_statuses('coingig')
#for status in statuses:
#    print
#    print status
#
#print "\n" * 3
#
##
#
#statuses = get_statuses('hypewizard')
#for status in statuses:
#    #print status
#    tweet = status
#    #print ts
#    if tweet.retweeted_status:
#        print tweet.retweeted_status
#
#        if tweet.retweeted_status.id == int(search_target_twitter_status_id): 
#            print '%s %s %s\n' % (
#                    tweet.retweeted_status.id, 
#                    convert_twitter_timestamp(tweet.retweeted_status.created_at), 
#                    convert_twitter_timestamp(tweet.retweeted_status.created_at)
#                ) * 20 

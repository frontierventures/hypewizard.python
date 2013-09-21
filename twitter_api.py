import json
import time, datetime
import twitter

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

def convert_twitter_timestamp(created_at):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
    return timestamp

def get_status(status_id):
    status = api.GetStatus(status_id, trim_user=True, include_my_retweet=True, include_entities=True)
    return status

def get_retweets(status_id):
    statuses = api.GetRetweets(status_id, count=100, trim_user=False) 
    return statuses

status_id = '380866222369144832' # Client Status Id 
screen_name = 'hypewizard'

#from datetime import datetime, date, time
from dateutil.parser import parse
from datetime import datetime

def is_promotional_period_over(status_id, screen_name):
    statuses = get_retweets(status_id)
    for status in statuses:
        if status.user.screen_name == screen_name:
            #print status.created_at, convert_twitter_timestamp(status.created_at)
            #print status.user.time_zone, status.user.utc_offset
    
            dt1 = parse(status.created_at)
            dt1 = dt1.replace(tzinfo=None)
            seconds1 = (dt1 - datetime(1970,1,1)).total_seconds()
    
            dt2 = datetime.utcnow() #current utc time 
            seconds2 = (dt2 - datetime(1970,1,1)).total_seconds()
    
            delta = seconds2 - seconds1
    
            if delta < 86400:
                print "You have about %s to go until the end of promotion." % int(24 - delta / 3600)

is_promotional_period_over(status_id, screen_name)

        
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

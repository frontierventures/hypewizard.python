import twitter
import json

api = twitter.Api()

api = twitter.Api(consumer_key='PZbYciNC8TS3LVxeHaBTg',
                  consumer_secret='o4sKqGuCkuVnlTTiYe4FcHC82UtGprdZVGqjyMGz18',
                  access_token_key='632058592-trS5QTBYedptP4AFik4w1mwFcId74EK5qBy1VbHE',
                  access_token_secret='SUIZajSIznRzvPWNKUgkGPZnLlyXLTYq5YvLZVGrq4M')

#print api.VerifyCredentials()
#
#statuses = api.GetUserTimeline(screen_name="coingig")
#print [s.text for s in statuses]
#print
#
#statuses = api.GetUserTimeline(screen_name="money_powder")
#print [s.text for s in statuses]
#print
#
#followers = api.GetFollowers(screen_name="money_powder", include_user_entities=False)
#print [s.screen_name for s in followers]
##print followers
#print

def get_followers_count(twitter_name):
    user = api.GetUser(screen_name=twitter_name)
    return user.followers_count
    #print [s.text for s in statuses]
    #print user, type(user)
    #print user.followers_count
    #print json.dumps(user)

def get_statuses(twitter_name):
    # user = api.GetUser(screen_name="coingig")
    statuses = api.GetUserTimeline(screen_name=twitter_name)
    return statuses

def get_user(twitter_name):
    user = api.GetUser(screen_name=twitter_name)
    return user


#user = api.GetUser(screen_name="money_powder")
#print user.followers_count

#information = api.UsersLookup(screen_name="coingig")
#print statuses
#
#for status in statuses:
#    print status.id, status.text

#  93     status.created_at
#    94     status.created_at_in_seconds # read only
#      95     status.favorited
#        96     status.favorite_count
#          97     status.in_reply_to_screen_name
#            98     status.in_reply_to_user_id
#              99     status.in_reply_to_status_id
#               100     status.truncated
#                101     status.source
#                 102     status.id
#                  103     status.text
#                   104     status.location
#                    105     status.relative_created_at # read only
#                     106     status.user
#                      107     status.urls
#                       108     status.user_mentions
#                        109     status.hashtags
#                         110     status.geo
#                          111     status.place
#                           112     status.coordinates
#                            113     status.contributors
#

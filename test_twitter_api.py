import twitter_api
   
def match(tweets, status_id):
    for tweet in tweets:
        if tweet.retweeted_status:
            print tweet.retweeted_status
    
            if tweet.retweeted_status.id == int(status_id): 
                print '%s %s %s\n' % (
                        tweet.retweeted_status.id, 
                        twitter_api.convert_twitter_timestamp(tweet.retweeted_status.created_at), 
                        twitter_api.convert_twitter_timestamp(tweet.retweeted_status.created_at)
                    ) * 20 

if __name__ == '__main__':
    #account = CoinbaseAccount(api_key=API_KEY)
    #test_get_rates(account=account)
    #test_create_invoice(account=account)
    #print twitter_api.get_followers_count('coingig')
    #print twitter_api.get_user('hypewizard')['user']

    #print twitter_api.get_statuses('hypewizard')
    #print
    #statuses = twitter_api.get_statuses('helper_alice')

    #for status in statuses:
    #    print status
    
    # twitter for promotion
    status_id = '381333411018715136'
    client_id = '632058592'

    tweets = twitter_api.get_statuses('helper_alice')

    match(tweets, status_id)
    
    # Find retweets

'''
print twitter_api.get_user('helper_alice')['user']
{
   "created_at":"Mon Sep 23 21:05:59 +0000 2013",
   "id":1898382054,
   "lang":"en",
   "name":"Test Test",
   "profile_background_color":"C0DEED",
   "profile_background_tile":false,
   "profile_image_url":"https://abs.twimg.com/sticky/default_profile_images/default_profile_2_normal.png",
   "profile_link_color":"0084B4",
   "profile_sidebar_fill_color":"http://abs.twimg.com/images/themes/theme1/bg.png",
   "profile_text_color":"333333",
   "protected":false,
   "screen_name":"helper_alice"
}
{
   "created_at":"Tue Jul 10 15:03:07 +0000 2012",
   "description":"Somewhere between a chimpanzee and a robot...",
   "favourites_count":9,
   "followers_count":8,
   "friends_count":50,
   "id":632058592,
   "lang":"en",
   "name":"Frontier Ventures",
   "profile_background_color":"C0DEED",
   "profile_background_tile":false,
   "profile_image_url":"https://si0.twimg.com/profile_images/378800000485472101/27c7a9dc98a6aaaa1e208c242bcb3666_normal.png",
   "profile_link_color":"0084B4",
   "profile_sidebar_fill_color":"http://abs.twimg.com/images/themes/theme1/bg.png",
   "profile_text_color":"333333",
   "protected":false,
   "screen_name":"hypewizard",
   "status":{
      "created_at":"Sat Sep 21 15:45:21 +0000 2013",
      "favorited":false,
      "id":381444044376666114,
      "retweeted":false,
      "source":"web",
      "text":"test",
      "truncated":false
   },
   "statuses_count":12,
   "time_zone":"Mountain Time (US & Canada)",
   "utc_offset":-21600
}
'''

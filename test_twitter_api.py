import twitter_api
   
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

if __name__ == '__main__':
    client_id = '632058592'

    #status_id = '382245592719568896'
    # You can search promoters timeline and see which are retweets
    # You can search clients timeline and see what was retweeted

    tweets = twitter_api.get_statuses('hypewizard')
    print tweets
    #print twitter_api.get_timeline(client_id)

    promoter_id = '1898591701' 
    status_id = '381333411018715136'

    #verify_transaction(promoter_id, status_id)
    #twitter_api.is_promotional_period_over(promoter_id, status_id)
    #match(tweets, status_id)
    
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

from twython import TwythonStreamer
import config

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code, data

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()


stream = MyStreamer(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN_KEY, config.ACCESS_TOKEN_SECRET)
#stream.statuses.filter(track='hypewizard')
#stream.user(track='hypewizard')
#stream.site(track='hypewizard')
#stream.site(follow='hypewizard')
stream.statuses.filter(follow=632058592)


#curl --request 'POST' 'https://stream.twitter.com/1.1/statuses/filter.json' --data 'follow=632058592' --header 'Authorization: OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="8ca682473db85d75ff5e30cb301d66a1", oauth_signature="HFV7zo4u66NcQgp1FK2RwoUVyDs%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1379744547", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"' --verbose

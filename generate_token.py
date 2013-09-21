#STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
#PARAMS = {
#    'follow': '632058592'
#}
#METHOD = 'post'
#
#print create_signature_base(STREAM_URL, PARAMS, METHOD) 
#print
#print create_header_string(STREAM_URL, PARAMS, METHOD) 

#print '\n';
#print oauth.signatureBaseForRequest(url, params, method);
#print '\n';
#print oauth.headerStringForRequest(url, params, method);
#print '\n';

import oauth2 as oauth
import config

# Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key=config.CONSUMER_KEY, secret=config.CONSUMER_SECRET)

# Request token URL for Twitter.
request_token_url = "http://twitter.com/oauth/request_token"
request_token_url = 'https://api.twitter.com/oauth/request_token'

## Create our client.
#client = oauth.Client(consumer)
#
#resp, content = client.request(request_token_url, "GET")
#print resp
#print
#print content
#
#
#def generate_nonce():
#    random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
#    m = md5.new(str(time()) + str(random_number))
#    return m.hexdigest()
#
##print generate_nonce()
#
#
#print data

#data = {
#    "oauth_timestamp" : str(int(time())),
#    "oauth_version" : "1.0",
#    "oauth_signature_method": "HMAC-SHA1",
#    "oauth_consumer_key": config.CONSUMER_KEY,
#
#    }
#HEADER = 'Authorization: OAuth 
#oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", 
#oauth_nonce="1f502d619fc1b0e21c42c645b0d511cd", 
#oauth_signature="yx64GmrXuQkC%2BO5UgmlLAGPAGJs%3D", 
#oauth_signature_method="HMAC-SHA1", 
#oauth_timestamp="1379751873", 
#oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", 
#oauth_version="1.0"'

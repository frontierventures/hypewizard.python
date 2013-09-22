import oauth2 as oauth
import urlparse 
 
#OAUTH_KEYS = {
#    'access_token_key': '',
#    'access_token_secret': ''
#   }
#TOKEN_URL = 'https://coinbase.com/oauth/token'
#
#consumer = oauth.Consumer(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
#client = oauth.Client(consumer)
#
#resp, content = client.request(TOKEN_URL, "POST")
#
#print resp
#print content
#
#if resp['status'] != '200':
#    raise Exception("Invalid response %s." % resp['status'])
#     
#request_token = dict(urlparse.parse_qsl(content))
#
#print request_token
import urllib
import urllib2
auth_code = raw_input('Enter authorization code (parameter of URL): ')

client_id = '17325ef5deacbce04f75e9d794704b306de7b84811d2404074d2c9557fb2deef'
client_secret = '4b97114ef405c03410e2e9f27036f1729449671233aea0ff1596f0a7baa0b2d2'
redirect_uri = 'https://bitcoinrealty.ca/callback' 

data = urllib.urlencode({
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
})

TOKEN_URL = 'https://coinbase.com/oauth/token'
print TOKEN_URL
request = urllib2.Request(
    url=TOKEN_URL,
    data=data)
request_open = urllib2.urlopen(request)

#6. Google returns access token, refresh token, and expiration of
#   access token
response = request_open.read()
request_open.close()
tokens = json.loads(response)
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

#7. Access token can be used for all subsequent requests to Fusion Tables,
##   until the token expires
#request = urllib2.Request(
#  url='https://www.google.com/fusiontables/api/query?%s' % \
#    (urllib.urlencode({'access_token': access_token,
#                       'sql': 'SELECT * FROM 123456'})))
#request_open = urllib2.urlopen(request)
#response = request_open.read()
#request_open.close()
#print response
#
##8. When the access token expires,
##   the refresh token is used to request a new access token
#data = urllib.urlencode({
#  'client_id': client_id,
#  'client_secret': client_secret,
#  'refresh_token': refresh_token,
#  'grant_type': 'refresh_token'})
#request = urllib2.Request(
#  url='https://accounts.google.com/o/oauth2/token',
#  data=data)
#request_open = urllib2.urlopen(request)
#response = request_open.read()
#request_open.close()
#tokens = json.loads(response)
#access_token = tokens['access_token']
#
##def oauth_req(url, key, secret, http_method="GET", post_body=None, http_headers=None):
##    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
##    token = oauth.Token(key=key, secret=secret)
##    client = oauth.Client(consumer, token)
## 
##    resp, content = client.request(
#        url,
#        method=http_method,
#        body=post_body,
#        headers=http_headers,
#        force_auth_header=True
#    )
#    return content
#
#print oauth_req(TOKEN_URL, OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])

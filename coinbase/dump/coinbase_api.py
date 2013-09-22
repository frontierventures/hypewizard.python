import time
import pycurl
import cStringIO
import urllib
import json
import oauth2 as oauth

API_KEY = '61ce7b714190bfbc77a4fa104837b7c5a1323677697a7d9275506445dceed6dd'

CLIENT_ID = ''
CLIENT_SECRET = ''

import time
import pycurl
import urllib
import json
import oauth2 as oauth
 
#API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
#API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
API_ENDPOINT_URL = 'https://coinbase.com/api/v1/account/balance' 
USER_AGENT = 'AGENT 1.0' # This can be anything really
 
# You need to replace these with your own values
OAUTH_KEYS = {'consumer_key': '17325ef5deacbce04f75e9d794704b306de7b84811d2404074d2c9557fb2deef',
              'consumer_secret': '4b97114ef405c03410e2e9f27036f1729449671233aea0ff1596f0a7baa0b2d2',
              'access_token_key': '',
              'access_token_secret': ''}
 
# These values are posted when setting up the connection
POST_PARAMS = {'include_entities': 0,
               'stall_warning': 'true',
               'track': 'iphone,ipad,ipod'}
 
class Client:
    def __init__(self):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.setup_connection()
 
    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''

        response = cStringIO.StringIO()
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
        #self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        self.conn.setopt(pycurl.VERBOSE, True)
        # self.handle_tweet is the method that are called when new tweets arrive
        #self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)
        self.conn.setopt(pycurl.WRITEFUNCTION, response.write)
        self.conn.perform()
           
        #print response.getValue()
        #http_code = conn.getinfo(pycurl.HTTP_CODE)
        #if http_code is 200:
        #    invoice = response.getvalue()
        #    invoice = json.loads(invoice)
        #    print invoice
        #    print invoice.keys()

    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        #req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_URL,
        #                                                                     urllib.urlencode(POST_PARAMS)))
        #req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        req = oauth.Request(method='GET', parameters=params, url='%s' % API_ENDPOINT_URL)
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

c = Client()

#c.setup_connection()
#
#print get_oauth_header()

#import pycurl
#import cStringIO
#import base64
#import json
#import urllib
#
#
#post_params = [
#    ('ASYNCPOST',True),
#    ('PREVIOUSPAGE','yahoo.com'),
#    ('EVENTID',5),
#]
#post_params = [
#    ('price',10),
#    ('currency','USD'),
#    ('notificationURL','https://bitcoinrealty.ca/receiver'),
#    ('fullNotifications', 'true'),
#    ('posData', '{"id": 1}'),
#]
#resp_data = urllib.urlencode(post_params)
#resp_data = 'price=10&currency=USD&notificationURL=https://bitcoinrealty.ca/receiver&fullNotifications=true'
#
#
##mycurl.setopt(pycurl.POSTFIELDS, resp_data)
##mycurl.setopt(pycurl.POST, 1)
##ycurl.perform()
#
#URL = 'https://bitpay.com/api/'
#
##DATA = 'price=10&currency=USD'
#
##print DATA
#
#API_KEY = '39H3AR8j22u5esFZNljAc2Z7y5R4aBkstMAJPgmg4'
#headers = { 'Authorization' : 'Basic %s' % base64.b64encode(API_KEY) }
#
#def create_invoice():
#    URL = 'https://bitpay.com/api/invoice/'
#    response = cStringIO.StringIO()
#    conn = pycurl.Curl()
#    
#    conn.setopt(pycurl.VERBOSE, 1)
#    conn.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
#    
#    conn.setopt(pycurl.URL, URL)
#    conn.setopt(pycurl.POST, 1)
#    
#    #if DATA:
#    print resp_data
#    conn.setopt(pycurl.POSTFIELDS, resp_data)
#    
#    conn.setopt(pycurl.SSL_VERIFYPEER, 1)
#    conn.setopt(pycurl.SSL_VERIFYHOST, 2)
#    
#    conn.setopt(pycurl.WRITEFUNCTION, response.write)
#    
#    conn.perform()
#    
#    http_code = conn.getinfo(pycurl.HTTP_CODE)
#    if http_code is 200:
#        invoice = response.getvalue()
#        invoice = json.loads(invoice)
#        print invoice
#        print invoice.keys()
#
#
#def get_invoice(invoice_id):
#    URL = 'https://bitpay.com/api/invoice/%s' % invoice_id
#    response = cStringIO.StringIO()
#    conn = pycurl.Curl()
#    
#    conn.setopt(pycurl.VERBOSE, 1)
#    conn.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
#    
#    conn.setopt(pycurl.URL, URL)
#    
#    conn.setopt(pycurl.SSL_VERIFYPEER, 1)
#    conn.setopt(pycurl.SSL_VERIFYHOST, 2)
#    
#    conn.setopt(pycurl.WRITEFUNCTION, response.write)
#    
#    conn.perform()
#    
#    http_code = conn.getinfo(pycurl.HTTP_CODE)
#    if http_code is 200:
#        invoice = response.getvalue()
#        invoice = json.loads(invoice)
#        print invoice
#        print invoice.keys()
#
#def get_balance():
#    #URL = 'https://coinbase.com/api/v1/account/balance?api_key=%s' % API_KEY
#    API_KEY = '61ce7b714190bfbc77a4fa104837b7c5a1323677697a7d9275506445dceed6dd'
#    headers = { 'Authorization' : 'Basic %s' % base64.b64encode(API_KEY) }
#    headers = { 'Authorization' : 'OAuth %s' % base64.b64encode(API_KEY) }
#    headers = { 'Authorization' : 'OAuth %s' % API_KEY }
#    headers = { 'Authorization' : 'Basic %s' % API_KEY }
#    URL = 'https://coinbase.com/api/v1/account/balance'
#
#    response = cStringIO.StringIO()
#    conn = pycurl.Curl()
#    
#    conn.setopt(pycurl.VERBOSE, 1)
#    conn.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
#    
#    conn.setopt(pycurl.URL, URL)
#    
#    conn.setopt(pycurl.SSL_VERIFYPEER, 1)
#    conn.setopt(pycurl.SSL_VERIFYHOST, 2)
#    
#    conn.setopt(pycurl.WRITEFUNCTION, response.write)
#    
#    conn.perform()
#    
#    http_code = conn.getinfo(pycurl.HTTP_CODE)
#    if http_code is 200:
#        invoice = response.getvalue()
#        invoice = json.loads(invoice)
#        print invoice
#        print invoice.keys()
#
##get_invoice('5yk7JSVao6NTnd72EY42oY')
##create_invoice()
#get_balance()

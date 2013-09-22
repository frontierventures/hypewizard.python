from oauth2client.client import OAuth2WebServerFlow
import httplib2
import sys

CLIENT_ID = '1e6dc802a76840817a9055a49dc86ae801ad4b474d5a97a1b7dce1e3cc01b1bc'
CLIENT_SECRET = '00579619f736854a922e18d2652e6608cad3f83abe0d8e3327b3c588905314e1'
CALLBACK_URL = 'https://www.bitcoinrealty.ca/callback'

coinbase_client = OAuth2WebServerFlow(
        CLIENT_ID, 
        CLIENT_SECRET, 
        'all', 
        redirect_uri=CALLBACK_URL, 
        auth_uri='https://coinbase.com/oauth/authorize', 
        token_uri='https://coinbase.com/oauth/token'
)

#oauth_code = 'b4b17f6530fbdc0bebfd9ec634adee098a9570e2a432cf9a5dcae878cb47ace4'
#oauth_code = 'b9aa9fd861e01e19bec01b4973a1e013b3cb4490418d0968018a47d0b3678da9'
#oauth_code = '878ad25bdff99cf85de86ab77ef1495ad706c7133703344edd92ce08a69be9de'
#http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')
#token = coinbase_client.step2_exchange(oauth_code, http=http)
#token = coinbase_client.step2_exchange(oauth_code, http=None)
#print token.to_json()

if __name__ == "__main__":
    print "[0] create authorization url"
    print "[1] generate credentials"
    print sys.argv

    if sys.argv[1] == '0':
        auth_url = coinbase_client.step1_get_authorize_url()
        print auth_url

    if sys.argv[1] == '1':
        oauth_code = sys.argv[2]
        token = coinbase_client.step2_exchange(oauth_code, http=None)
        print token.to_json()

#import time
#import pycurl
#import cStringIO
#import urllib
#import json
#import oauth2 as oauth
# 
#class Client:
#    def __init__(self):
#        self.auth_url = coinbase_client.step1_get_authorize_url()
#        self.conn = None
#        self.buffer = ''
#        self.setup_connection()
# 
#    def setup_connection(self):
#        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
#        """
#        if self.conn:
#            self.conn.close()
#            self.buffer = ''
#
#        response = cStringIO.StringIO()
#        self.conn = pycurl.Curl()
#        self.conn.setopt(pycurl.URL, auth_url)
#        self.conn.setopt(pycurl.WRITEFUNCTION, response.write)
#        self.conn.perform()
#           
#        print response.getvalue()
#        print response
#        #http_code = conn.getinfo(pycurl.HTTP_CODE)
#        #if http_code is 200:
#        #    invoice = response.getvalue()
#        #    invoice = json.loads(invoice)
#        #    print invoice
#        #    print invoice.keys()
#
#c = Client()

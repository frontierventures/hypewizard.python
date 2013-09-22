import pycurl
import cStringIO
import base64
import json
import urllib
import cgi

post_params = [
    ('client_id','17325ef5deacbce04f75e9d794704b306de7b84811d2404074d2c9557fb2deef'),
    ('client_secret', '4b97114ef405c03410e2e9f27036f1729449671233aea0ff1596f0a7baa0b2d2'),
    ('redirect_uri', 'none'),
    ('grant_type','authorization_code'),
    ('code', 'none'),
]

args = {}
args['client_id'] = '17325ef5deacbce04f75e9d794704b306de7b84811d2404074d2c9557fb2deef'
args['client_id'] = '8b0b1a26509950c6fe196b250b2e65ff116c9b9ea46a17d9ed2cc3b75aff4f0ap'
args['client_secret'] = '4b97114ef405c03410e2e9f27036f1729449671233aea0ff1596f0a7baa0b2d2'
args['client_secret'] = 'c8c63a64d511895bcb7e11928328a157efae970da8bc9d7f3dc03d9bd77956a9'
args['redirect_uri'] = 'https://www.bitcoinrealty.ca/callback'
args['grant_type'] = 'authorization_code'
args['code'] = 'none'

resp_data = urllib.urlencode(args)

URL = 'https://coinbase.com/oauth/token'
print URL
#URL = 'https://coinbase.com/oauth/token?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s&client_secret=%s' % (args['code'], args['redirect_uri'], args['client_id'], args['client_secret'])
#URL = 'https://coinbase.com/oauth/token?client_id=17325ef5deacbce04f75e9d794704b306de7b84811d2404074d2c9557fb2deef&client_secret=4b97114ef405c03410e2e9f27036f1729449671233aea0ff1596f0a7baa0b2d2&redirect_uri=none&grant_type=authorization_code&code=none'

#headers = { 'Authorization' : 'Basic %s' % base64.b64encode(API_KEY) }

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#args["client_secret"] = FACEBOOK_APP_SECRET  #facebook APP Secret
#args["code"] = self.request.get("code")
response = cgi.parse_qs(urllib.urlopen(URL).read())
print response
#    "https://graph.facebook.com/oauth/access_token?" +
#    urllib.urlencode(args)).read())
#access_token = response["access_token"][-1]

def create_invoice():
    response = cStringIO.StringIO()
    conn = pycurl.Curl()
    
    conn.setopt(pycurl.VERBOSE, 1)
    conn.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
    
    conn.setopt(pycurl.URL, URL)
    conn.setopt(pycurl.POST, 1)
    
    print resp_data
    conn.setopt(pycurl.POSTFIELDS, resp_data)
    
    conn.setopt(pycurl.SSL_VERIFYPEER, 1)
    conn.setopt(pycurl.SSL_VERIFYHOST, 2)
    
    conn.setopt(pycurl.WRITEFUNCTION, response.write)
    
    conn.perform()
    
    http_code = conn.getinfo(pycurl.HTTP_CODE)
    if http_code is 200:
        invoice = response.getvalue()
        #invoice = json.loads(invoice)
        print invoice
        #print invoice.keys()

create_invoice()

#url = "https://coinbase.com/api/v1/transactions/send_money?access_token=XXX"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#params = {
#             "transaction": { 
#                 "to": "1G8f9pRvgprVMUymuQugZrhYSqBNXuwzNt", 
#                 "amount": "0.011", 
#                 "notes": "Testing transaction" 
#             }
#         }
#
#r = requests.post(url, data=json.dumps(postData), headers=headers)

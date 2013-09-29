import pycurl, json
import config
import sign_request

STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
PARAMS = {'follow': '1898591701'}
METHOD = 'post'


string =  sign_request.create_header_string(STREAM_URL, PARAMS, METHOD) 

print
print string
print 

#string = 'OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="bc97b9b9575471b8432bdd2d29dc67a7", oauth_signature="j33HyaYoNuI8qMJM%2BDO4%2F5ABlsc%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1380389414", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"'

#string ='OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="bc97b9b9575471b8432bdd2d29dc67a7", oauth_signature="j33HyaYoNuI8qMJM%2BDO4%2F5ABlsc%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1380389414", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"'

#string = 'OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="639754320322ffa434dbf4dd187d769f", oauth_signature="OfdhXqbCrDd2enT8vxSkKYWjDvo%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1380390550", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"'

HEADER = 'Authorization: %s' % string 
#DATA = 'follow=632058592'
DATA = 'follow=1898591701'


class Client:
  def __init__(self):
    self.buffer = ""
    self.conn = pycurl.Curl()
    self.conn.setopt(pycurl.URL, STREAM_URL)
    self.conn.setopt(pycurl.HTTPHEADER, [HEADER])
    self.conn.setopt(pycurl.POSTFIELDS, DATA)
    self.conn.setopt(pycurl.VERBOSE, True)
    self.conn.perform()

  def on_receive(self, data):
    self.buffer += data
    if data.endswith("rn") and self.buffer.strip():
      content = json.loads(self.buffer)
      self.buffer = ""
      print content['created_at']
    

client = Client()

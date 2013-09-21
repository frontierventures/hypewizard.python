#curl --request 'POST' 'https://stream.twitter.com/1.1/statuses/filter.json' --data 'follow=632058592' --header 'Authorization: OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="8ca682473db85d75ff5e30cb301d66a1", oauth_signature="HFV7zo4u66NcQgp1FK2RwoUVyDs%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1379744547", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"' --verbose

#curl --request 'POST' 'https://stream.twitter.com/1.1/statuses/filter.json' --data 'follow=632058592' --header 'Authorization: OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="e20eb031e7a054f6968decf18b091c23", oauth_signature="vDzVtfbXnmPAUMnHnZjdwLLYMC8%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1379750822", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"' --verbose

import pycurl, json
import config

STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'

DATA = 'follow=632058592'

HEADER = 'Authorization: OAuth oauth_consumer_key="Ph8ahj5i3V4ZaT9HT334Yg", oauth_nonce="1f502d619fc1b0e21c42c645b0d511cd", oauth_signature="yx64GmrXuQkC%2BO5UgmlLAGPAGJs%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1379751873", oauth_token="632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l", oauth_version="1.0"'


class Client:
  def __init__(self):
    self.buffer = ""
    self.conn = pycurl.Curl()
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

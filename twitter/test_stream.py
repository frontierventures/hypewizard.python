import pycurl, json
import config
import sign_request

STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
PARAMS = {'follow': '632058592'}
METHOD = 'post'

HEADER = 'Authorization: %s' % sign_request.create_header_string(STREAM_URL, PARAMS, METHOD) 
DATA = 'follow=632058592'

print HEADER

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

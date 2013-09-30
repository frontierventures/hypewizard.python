import pycurl
import sys
import sign_request
import json
#import get_tweets


STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
PARAMS = {'follow': '1898591701'}
METHOD = 'post'

string =  sign_request.create_header_string(STREAM_URL, PARAMS, METHOD) 
HEADER = 'Authorization: %s' % string 
DATA = 'follow=1898591701'


from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection['hypewizard']
tweets = db['tweets']

class Header:
    def __init__(self):
        self.contents = ''
        self.line = 0
        self.content = ''

    def process(self, data):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, data)
        print self.contents

    def __str__(self):
        return self.contents

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0
        self.content = ''

    def process_body(self, data):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, data)
        print self.contents
        tweet = self.assemble(data)
        self.process_tweet(tweet)

    def assemble(self, data):
        """
            Need this function in case response is returned partially
        """
        self.content += data
        output = json.loads(self.content)
        self.content = ""
        return output

    def process_tweet(self, tweet):
        print "id: %s" % tweet['id']
        tweets.insert(tweet)

    def __str__(self):
        return self.contents

class Debug:
    def __init__(self):
        self.contents = ''
        self.line = 0
        self.content = ''

    def process(self, data):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, data)
        print self.contents

    def __str__(self):
        return self.contents

header = Header()
storage = Storage()
debug = Debug()

c = pycurl.Curl()
c.setopt(c.URL, STREAM_URL)
c.setopt(c.HTTPHEADER, [HEADER])
c.setopt(c.POSTFIELDS, DATA)
c.setopt(c.WRITEFUNCTION, storage.process_body)
c.setopt(c.HEADERFUNCTION, header.process)
c.setopt(c.DEBUGFUNCTION, debug.process)
c.perform()

import pycurl
import sys
import sign_request
import json
import collections
from pymongo import Connection


STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
PARAMS = {'follow': '1898591701'}
METHOD = 'post'

string =  sign_request.create_header_string(STREAM_URL, PARAMS, METHOD) 
HEADER = 'Authorization: %s' % string 
DATA = 'follow=1898591701'


connection = Connection('localhost', 27017)
db = connection['hypewizard']

twitter_data = db['twitter_data']
keywords = db['keywords']

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

        try:
            tweet = self.assemble(data)
        except Exception as e:
            print e
            return

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
        print "text: %s" % tweet['text']
        data = {
            'uid': 0,
            'pid': tweet['user']['id'], 
            'tweet_id': tweet['id'],
            'text': tweet['text']
        }
        twitter_data.insert(data)
        print "data: %s => twitter_data" % data 

        # Update current keywords
        words = tweet['text'].split() 

        counter = collections.Counter(words)
        data = dict(counter)

        keywords.insert(data)
        print "data: %s => keywords" % data 

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

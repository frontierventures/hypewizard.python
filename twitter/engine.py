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

        uid = 1

        data = {
            'uid': uid,
            'pid': tweet['user']['id'], 
            'tweet_id': tweet['id'],
            'text': tweet['text'] 
        }

        twitter_data.insert(data)
        print "data: %s => twitter_data" % data 

        # Update current keywords
        words = tweet['text'].split() 

        # count words
        counter = collections.Counter(words)
        counts = dict(counter)

        #entry = db.keywords.find({uid: 1})

        # CHECK THERE ARE WORDS THAT NEED TO BE INSERTED
        # PULL ALL KEYS

        record = keywords.find_one({'uid': 1})

        if record:
            # current_keys for the user
            current_keys = record['counts'].keys()
            print "current_keys: %s" % current_keys

            new_keys = counts.keys()
            print "new_keys: %s" % new_keys

            #difference = list(set(current_keys) - set(new_keys)) 
            #print "difference: %s" % difference

            #difference = list(set(new_keys) - set()) 
            #print "difference: %s" % difference
            
            for key in new_keys:
                if key not in current_keys:
                    print "word: %s not in database" % key
                else:
                    print "word: %s is in database" % key

            

            #record = keywords.find_one({'uid': 1})

            #if 'ted' in keys: 
            #    print "FOUND"

            #if 'bob' in keys: 
            #    print "FOUND"

            # CHECK RECORD ONE BY ONE

            # INSERT KEYS IF NEEDED
            #cursor = keywords.find({'counts.ted': {'$exists': True}})
            #cursor = keywords.find({'counts.ted': {'$exists': True}})
            #cursor = keywords.find({'counts.bob': {'$exists': True}})
            #print cursor

            #does_key_exit = False
            #if cursor.count() > 0:
            #    print "Key exists"
            #    does_key_exist = True
            print "Entry updated"

        else:
            data = {
                'uid': uid,
                'counts': counts
            }

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

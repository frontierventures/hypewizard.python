import pycurl
import sys
import sign_request
import json

STREAM_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
PARAMS = {'follow': '1898591701'}
METHOD = 'post'

string =  sign_request.create_header_string(STREAM_URL, PARAMS, METHOD) 
HEADER = 'Authorization: %s' % string 
DATA = 'follow=1898591701'


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

class Body:
    def __init__(self):
        self.contents = ''
        self.line = 0
        self.content = ''

    def process(self, data):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, data)
        print self.contents
        print "id: %s" % self.store(data)

    def store(self, data):
        """
            Need this function in case response is returned partially
        """
        self.content += data
        output = json.loads(self.content)
        self.content = ""
        return output['id']

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
body = Body()
debug = Debug()

c = pycurl.Curl()
c.setopt(c.URL, STREAM_URL)
c.setopt(c.HTTPHEADER, [HEADER])
c.setopt(c.POSTFIELDS, DATA)
c.setopt(c.WRITEFUNCTION, body.process)
c.setopt(c.HEADERFUNCTION, header.process)
c.setopt(c.DEBUGFUNCTION, debug.process)
c.perform()

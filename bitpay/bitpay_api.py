import pycurl
import cStringIO
import base64
import json
import urllib


post_params = [
    ('ASYNCPOST',True),
    ('PREVIOUSPAGE','yahoo.com'),
    ('EVENTID',5),
]
post_params = [
    ('price',10),
    ('currency','USD'),
    ('notificationURL','https://bitcoinrealty.ca/receiver'),
    ('fullNotifications', 'true'),
    ('posData', '{"id": 1}'),
]
resp_data = urllib.urlencode(post_params)
resp_data = 'price=10&currency=USD&notificationURL=https://bitcoinrealty.ca/receiver&fullNotifications=true'


#mycurl.setopt(pycurl.POSTFIELDS, resp_data)
#mycurl.setopt(pycurl.POST, 1)
#ycurl.perform()

URL = 'https://bitpay.com/api/'

#DATA = 'price=10&currency=USD'

#print DATA

API_KEY = '39H3AR8j22u5esFZNljAc2Z7y5R4aBkstMAJPgmg4'
headers = { 'Authorization' : 'Basic %s' % base64.b64encode(API_KEY) }

def create_invoice():
    URL = 'https://bitpay.com/api/invoice/'
    response = cStringIO.StringIO()
    conn = pycurl.Curl()
    
    conn.setopt(pycurl.VERBOSE, 1)
    conn.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
    
    conn.setopt(pycurl.URL, URL)
    conn.setopt(pycurl.POST, 1)
    
    #if DATA:
    print resp_data
    conn.setopt(pycurl.POSTFIELDS, resp_data)
    
    conn.setopt(pycurl.SSL_VERIFYPEER, 1)
    conn.setopt(pycurl.SSL_VERIFYHOST, 2)
    
    conn.setopt(pycurl.WRITEFUNCTION, response.write)
    
    conn.perform()
    
    http_code = conn.getinfo(pycurl.HTTP_CODE)
    if http_code is 200:
        invoice = response.getvalue()
        invoice = json.loads(invoice)
        print invoice
        print invoice.keys()


def get_invoice(invoice_id):
    URL = 'https://bitpay.com/api/invoice/%s' % invoice_id
    response = cStringIO.StringIO()
    conn = pycurl.Curl()
    
    conn.setopt(pycurl.VERBOSE, 1)
    conn.setopt(pycurl.HTTPHEADER, ["%s: %s" % t for t in headers.items()])
    
    conn.setopt(pycurl.URL, URL)
    
    conn.setopt(pycurl.SSL_VERIFYPEER, 1)
    conn.setopt(pycurl.SSL_VERIFYHOST, 2)
    
    conn.setopt(pycurl.WRITEFUNCTION, response.write)
    
    conn.perform()
    
    http_code = conn.getinfo(pycurl.HTTP_CODE)
    if http_code is 200:
        invoice = response.getvalue()
        invoice = json.loads(invoice)
        print invoice
        print invoice.keys()


#get_invoice('5yk7JSVao6NTnd72EY42oY')
create_invoice()

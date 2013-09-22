from urlparse import urlparse
from time import time

import config
import hashlib
import hmac
import md5
import random
import string
import urllib
import urllib2

def generate_nonce():
    random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
    m = md5.new(str(time()) + str(random_number))
    return str(m.hexdigest())

def create_signature_base(url, params, method):
    param_string = ""
    sorted_keys = sorted(params.iterkeys())
    for key in sorted_keys:
        string = '%s=%s' % (key, params[key])
        if param_string.__len__() > 0:
            param_string += "&" + string
        else:
            param_string = string

    params = urllib.quote_plus(param_string)
    
    url = urlparse(url)
    url = "https://stream.twitter.com" + url.path
    url = urllib.quote_plus(url)

    method = method.upper()
    
    signature_base = method + "&" + url + "&" + params
    return signature_base

def create_signature(url, params, method):
    signature_base = create_signature_base(url, params, method)
    signature_key = '%s&%s' % (config.CONSUMER_SECRET, config.ACCESS_TOKEN_SECRET)

    hashed = hmac.new(signature_key, signature_base, hashlib.sha1).digest()
    signature = hashed.encode('base64','strict')
    signature = signature[:-1] # remove newline

    return signature

def assemble_header_without_signature():
    nonce = generate_nonce()
    timestamp = str(int(round(time())))
    #nonce = 'e9909f2363207469a5354581db52655e'
    #timestamp = '1379775615'

    data = {
        "oauth_timestamp" : timestamp,
        "oauth_version" : "1.0",
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_consumer_key": config.CONSUMER_KEY,
        "oauth_nonce": nonce,
	    "oauth_token": config.ACCESS_TOKEN
    }
    return data

def create_header_string(url, params, method):
    headers = assemble_header_without_signature()

    for key in headers.iterkeys():
        params[key] = headers[key]
    
    headers["oauth_signature"] = create_signature(url, params, method)
    headers_keys = sorted(headers.iterkeys())
    
    header_string = "OAuth "

    for key in headers_keys:
        value = headers[key]
        string = urllib.quote_plus(key) + "=\"" + urllib.quote_plus(value) + "\", "
        header_string += string

    header_string = header_string[:-2]
    return header_string

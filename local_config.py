#!/usr/bin/env python
import os
import time
from datetime import datetime

mode = "prod" # dev | staging | prod | remote_dev

try:
    from config_local import mode
    print "imported local config", mode
except:
    pass


db_connection_string = ""
s3_key = ""
s3_password = ""
s3_bucket = ""

if mode == "prod":
    db_connection_string = 'postgres://postgres:ABC123ABC@localhost/coingig'
    s3_key = "AKIAINRPYCKNQ5QTEPKA"
    s3_password = "vLYmFAXmLIeLqabqhEZyEBPQCctShmIjNRAa1DGG"
    s3_bucket = 'coingig'

elif mode == "dev":
    db_connection_string = 'postgres://postgres:ABC123ABC@localhost/coingig'
    s3_key = "AKIAINRPYCKNQ5QTEPKA"
    s3_password = "vLYmFAXmLIeLqabqhEZyEBPQCctShmIjNRAa1DGG"
    s3_bucket = 'coingig-dev'

elif mode == "staging":
    db_connection_string = 'postgres://postgres:ABC123ABC@localhost/coingig_dev'
    s3_key = "AKIAINRPYCKNQ5QTEPKA"
    s3_password = "vLYmFAXmLIeLqabqhEZyEBPQCctShmIjNRAa1DGG"
    s3_bucket = 'coingig-dev'

elif mode == "remote_dev":
    db_connection_string = 'postgres://postgres:ABC123ABC@www.coingig.com/coingig_dev'
    s3_key = "AKIAINRPYCKNQ5QTEPKA"
    s3_password = "vLYmFAXmLIeLqabqhEZyEBPQCctShmIjNRAa1DGG"
    s3_bucket = 'coingig-dev'

class color:
    HEADER = '\033[1;45m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.BLUE = ''
        self.RED = ''
        self.ENDC = ''


def create_timestamp():
    return time.time()


def convertTimestamp(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%a %e %b %Y %r %Z"
    timestamp = utc.strftime(format)
    return timestamp


def convertTimestampToHours(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%H:%M:%S"
    timestamp = utc.strftime(format)
    #timestamp = time.strftime('%H:%M:%S', timestamp)
    return timestamp


def convertTimestampToDays(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%j:%H:%M:%S"
    timestamp = utc.strftime(format)
    #timestamp = time.strftime('%H:%M:%S', timestamp)
    return timestamp


cdn = 'https://s3.amazonaws.com/coingig/images'
cdnImages = 'https://s3.amazonaws.com/coingig/images'
cdnLogos = 'https://s3.amazonaws.com/coingig/logos'
#cdnLogos = '../images/stores'

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

CONSUMER_KEY = 'Ph8ahj5i3V4ZaT9HT334Yg' 
CONSUMER_SECRET = 'hHzGGTG4zXuMdI6H7mxEMKzBLSmbacb4MXCDG5Rd3ps'
ACCESS_TOKEN_KEY = '632058592-8ZTOQ3rr1EDyNbDNwJ10c0Iqr7jLeDkcXwvQn15l'
ACCESS_TOKEN_SECRET = 'WWdAWQQA0FBDmGsHyvRue8yy2tBQhQ9cNXsnXk'

if mode == "prod":
    db_connection_string = 'postgres://postgres:ABC123ABC@localhost/hypewizard'

elif mode == "dev":
    db_connection_string = 'postgres://postgres:ABC123ABC@localhost/hypewizard'

elif mode == "staging":
    db_connection_string = 'postgres://postgres:ABC123ABC@localhost/hypewizard_dev'

elif mode == "remote_dev":
    db_connection_string = 'postgres://postgres:ABC123ABC@www.hypewizard.com/hypewizard_dev'

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


STANDARD = "%a %e %b %Y %r %Z"
HOURS = "%a %e %b %Y %r %Z"
DAYS = "%a %e %b %Y %r %Z"

def convert_timestamp(timestamp, formatting):
    utc = datetime.utcfromtimestamp(float(timestamp))
    timestamp = utc.strftime(formatting)
    return timestamp

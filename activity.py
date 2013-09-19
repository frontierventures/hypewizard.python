#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from data import Log
from data import db

import config
from sessions import SessionManager


class Main(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        request.write("<!doctype html>")
        request.write("<title>Site-Wide Activity</title>")
        request.write("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js\">")
        request.write("</script>")
        request.write("<script src=\"../scripts/sendkeys.js\"></script>")
        #request.write("<input type=text id=entry value=\"type something\">")
        #request.write("<div id=output>Here you should see the typed text in UPPER case</div>")
        timestamp = config.create_timestamp()
        timestamp = config.convertTimestamp(float(timestamp))
        request.write("<div><b>Server Time:</b> %s</div>" % timestamp)
        request.write("<div><h1>Activity Log</h1></div>")
        request.write("<div id=log></div>")

        session_user = SessionManager(request).get_session_user()
        userType = session_user['type']
        if userType == 0:
            request.write("<div><h1>History</h1></div>")
            entries = db.query(Log).order_by(Log.timestamp.desc()).limit(10)

            for entry in entries:
                timestamp = config.convertTimestamp(float(entry.timestamp))
                request.write("<div><b>%s</b> %s</div>" % (timestamp, str(entry.entry)))

        request.finish()
        return NOT_DONE_YET


def createEntry(echoFactory, text):
    timestamp = config.create_timestamp()
    entry = "<b>%s</b> %s" % (timestamp, text)
    for connectedProtocol in echoFactory.connectedProtocols:
        connectedProtocol.dataReceived(entry)

    newEntry = Log(timestamp, text)
    db.add(newEntry)
    db.commit()

def pushToSocket(echoFactory, text):
    timestamp = config.create_timestamp()
    timestamp = config.convertTimestamp(float(timestamp))
    entry = "<b>%s</b> %s" % (timestamp, text)
    for connectedProtocol in echoFactory.connectedProtocols:
        connectedProtocol.dataReceived(entry)

def push_to_database(user_id, action, note):
    timestamp = config.create_timestamp()

    data = {
        'timestamp': timestamp,
        'user_id': user_id,
        'action': action,
        'note': note
        }

    new_log = Log(data)
    db.add(new_log)
    db.commit()

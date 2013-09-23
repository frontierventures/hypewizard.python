#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo

from sessions import SessionManager


class Main(Resource):
    def render_GET(self, request):
        session = request.getSession()
        SessionManager(request).clear_session_user()
        SessionManager(request).clearSessionSearch()
        SessionManager(request).clearSessionOrder()

        try:
            SessionManager(request).remove(session)
        except:
            print "ERROR"

        return redirectTo('../', request)

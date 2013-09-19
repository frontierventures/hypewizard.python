#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo

from sessions import SessionManager


class Main(Resource):
    def render_GET(self, request):
        session = request.getSession()
        SessionManager(request).clearSessionUser()
        SessionManager(request).clearSessionSearch()
        SessionManager(request).clearSessionProperty()
        SessionManager(request).clearSessionStore()
        SessionManager(request).clearSessionOrder()

        try:
            SessionManager(request).remove(session)
        except:
            print "ERROR"

        return redirectTo('../', request)

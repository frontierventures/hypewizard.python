#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User, Order
from data import db
from sessions import SessionManager

import config
import json
import forms
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_response = SessionManager(request).getSessionResponse()

        filters = {}

        Page = pages.Market('Market', 'market', filters)
        Page.session_user = session_user
        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.BLUE, session_response, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Market(Element):
    def __init__(self, session_user, filters):
        self.session_user = session_user
        self.filters = filters

        template = 'templates/elements/market.xml'
        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def view(self, request, tag):

        slots = {}
        slots['url1'] = '../feature_disabled?reason=not_authorized'
        slots['url2'] = '../feature_disabled?reason=not_authorized'

        if self.session_user['id'] != 0:
            slots['url1'] = '../process_ask?action=create' 
            slots['url2'] = '../process_bid?action=create' 
        yield tag.clone().fillSlots(**slots) 



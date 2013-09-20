#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User
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
        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['kind'] = request.args.get('kind')[0]
        except:
            filters['kind'] = 'client'

        Page = pages.Market('Market', 'market', filters)
        Page.session_user = session_user
        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.BLUE, session_response, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Table(Element):
    def __init__(self, session_user, filters):
        self.session_user = session_user
        self.filters = filters
        
        if filters['kind'] == 'promoter':
            template = 'templates/elements/promoter_orders_table.xml'
        
        if filters['kind'] == 'client':
            template = 'templates/elements/client_orders_table.xml'

        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def view(self, request, tag):

        slots = {}
        slots['url'] = '../feature_disabled?reason=not_authorized'
        slots['kind'] = self.filters['kind']

        if self.session_user['id'] != 0:
            if self.filters['kind'] == 'client':
                slots['url'] = '../process_ask?action=create' 

            if self.filters['kind'] == 'promoter':
                slots['url'] = '../process_bid?action=create' 
        yield tag.clone().fillSlots(**slots) 

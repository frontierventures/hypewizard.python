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


def assemble(root):
    root.putChild('feature_disabled', Process())
    return root


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
        
        if filters['kind'] == 'client':
            title = 'Promote Your Tweets with These Promoters' 
        if filters['kind'] == 'promoter':
            title = 'Earn by Promoting These Tweets for Our Clients' 

        Page = pages.Market(title, 'market', filters)
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
        if self.filters['kind'] == 'client':
            url = '../process_ask?action=create' 

        if self.filters['kind'] == 'promoter':
            url = '../process_bid?action=create' 

        slots = {}
        slots['kind'] = self.filters['kind']

        if self.session_user['status'] == 'unverified':
            url = '../feature_disabled?reason=unverified'

        if self.session_user['id'] == 0:
            url = '../feature_disabled?reason=unauthorized'

        slots['url'] = url

        yield tag.clone().fillSlots(**slots) 


class Process(Resource):
    def render(self, request):
        try:
            reason = request.args.get('reason')[0]
        except:
            return redirectTo('../', request)
        
        response = {}
        response['reason'] = reason

        if reason == 'unauthorized':
            response['message'] = 'You must be logged in to do this.'

        if reason == 'unverified':
            response['message'] = 'Please verify your email first.'

        return json.dumps(response)

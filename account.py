#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from sessions import SessionManager

import twitter_api
import config
import locale
import pages

from data import db
from sqlalchemy.sql import and_
from data import Profile
from sessions import SessionManager


def assemble(root):
    root.putChild('account', Main())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'account'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        Page = pages.Account('Account', 'account')
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Table(Element):
    def __init__(self, session_user, filters):
        self.session_user = session_user
        self.filters = filters

        template = 'templates/elements/ask_details.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.statuses = twitter_api.get_statuses(self.session_user['twitter_name'])

    @renderer
    def row(self, request, tag):
        for status in self.statuses:
            slots = {}
            slots['status_id'] = str(status.id)
            slots['status_text'] = status.text.encode('utf-8')
            self.status = status
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []
        buttons.append({
            'url': '../process_ask?action=create&status_id=%s' % self.status.id,
            'caption': 'Start Re-tweet Campaign' 
        })
        for button in buttons:
            slots = {}
            slots['caption'] = button['caption']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 


class Details(Element):
    def __init__(self, session_user):
        self.session_user = session_user

        self.profile = db.query(Profile).filter(Profile.id == session_user['id']).first()

        if session_user['status'] == 'verified':
            template = 'templates/elements/verified_account.xml'
        else:
            template = 'templates/elements/unverified_account.xml'

        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['slot_twitter_name'] = self.profile.twitter_name
        slots['slot_twitter_followers_count'] = str(twitter_api.get_followers_count(self.profile.twitter_name))
        yield tag.clone().fillSlots(**slots)

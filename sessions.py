#!/usr/bin/env python
from zope.interface import Interface, Attribute, implements
from twisted.web.resource import Resource
from twisted.python.components import registerAdapter
from twisted.web.server import Session

import config
import json
import random
import sys


sessions = set()
counter = []


class SessionManager():
    def __init__(self, request):
        self.request = request
        self.session = request.getSession()

    def _expired(self, session):
        print "Session", session.uid, "has expired."
        sessions.remove(session)

    def add(self):
        if self.session not in sessions:
            sessions.add(self.session)
            self.session.notifyOnExpire(lambda: self._expired(self.session))
        #sessionList.append(self.session)
        print "%ssession logged%s" % (config.color.BLUE, config.color.ENDC)

    def remove(self, session):
        session.expire()
        try:
            sessions.remove(session)
        except:
            pass
        print "%ssession removed%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionUid(self):
        request = self.request
        session = request.getSession()
        return session.uid

    def get_session_user(self):
        session_object = ISessionObject(self.session)
        return session_object.user

    def setSessionUser(self, user):
        session_object = ISessionObject(self.session)
        session_object.user = user

    def clear_session_user(self):
        session_object = ISessionObject(self.session)
        session_object.user = {
                'is_email_verified': False, 
                'id': 0, 
                'level': 1, 
                'twitter_name': '', 
                'transaction_count': 0, 
                'available_balance': 0, 
                'reserved_balance': 0
            }
        print "%ssession_user cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionSearch(self):
        session_object = ISessionObject(self.session)
        return session_object.search

    def setSessionSearch(self, search):
        session_object = ISessionObject(self.session)
        session_object.search = search

    def clearSessionSearch(self):
        session_object = ISessionObject(self.session)
        seed = random.randint(0, sys.maxint)
        session_object.search = {'seed': seed, 'isTabOpen': False, 'query': '', 'sort': 'top', 'categoryId': '', 'index': 1}
        print "%ssessionSearch cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionOrder(self):
        session_object = ISessionObject(self.session)
        return session_object.order

    def setSessionOrder(self, order):
        session_object = ISessionObject(self.session)
        session_object.order = order

    def clearSessionOrder(self):
        session_object = ISessionObject(self.session)
        session_object.order = {'id': 0}
        print "%ssessionOrder cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionTransaction(self):
        session_object = ISessionObject(self.session)
        return session_object.transaction

    def setSessionTransaction(self, transaction):
        session_object = ISessionObject(self.session)
        session_object.transaction = transaction

    def clearSessionTransaction(self):
        session_object = ISessionObject(self.session)
        session_object.transaction = {'id': 0}
        print "%ssessionTransaction cleared%s" % (config.color.BLUE, config.color.ENDC)

    def get_session_response(self):
        session_object = ISessionObject(self.session)
        return session_object.response

    def setSessionResponse(self, response):
        session_object = ISessionObject(self.session)
        session_object.response = response

    def clearSessionResponse(self):
        session_object = ISessionObject(self.session)
        session_object.response = {'class': 0, 'form': 0, 'text': ''}
        print "%ssession_response cleared%s" % (config.color.BLUE, config.color.ENDC)

    def setSearchResults(self, searchResults):
        session_object = ISessionObject(self.session)
        session_object.searchResults = searchResults

    def getSearchResuls(self):
        session_object = ISessionObject(self.session)
        return session_object.searchResults


class ISessionObject(Interface):
    user = Attribute('')
    search = Attribute('')
    order = Attribute('')
    response = Attribute('')
    searchResults = Attribute('')


class SessionObject(object):
    implements(ISessionObject)

    def __init__(self, session):
        self.user = {
                'is_email_verified': False, 
                'id': 0, 
                'level': 1, 
                'twitter_name': '', 
                'transaction_count': 0, 
                'available_balance': 0, 
                'reserved_balance': 0
            }
        seed = random.randint(0, sys.maxint)
        self.search = {'seed': seed, 'isTabOpen': False, 'query': '', 'sort': 'top', 'categoryId': '', 'index': 1}
        self.order = {'id': 0}
        self.transaction = {'id': 0}
        self.response = {'class': 0, 'form': 0, 'text': ''}
        self.searchResults = []


registerAdapter(SessionObject, Session, ISessionObject)


def disconnect(request, userId):
    buffer = set()
    for session in sessions:
        session_object = ISessionObject(session)
        session_user = session_object.user
        if session_user['id'] == userId:
            buffer.add(session)

    for session in buffer:
        SessionManager(request).remove(session)


#manager = Sessi\wonManager()
#print '%ssessions: %s%s' % (settings.color.RED, sessions.manager.uidList, settings.color.ENDC)
#activeUser = sessions.manager.getUserId(request)


class SessionTest(Resource):
    def render(self, request):

        session = request.getSession()
        thing = session.getComponent(ISessionObject, default='test')
        print thing.user
        uid = session.uid
        return uid
        #session_user = SessionManager(request).get_session_user()
        #user = json.dumps(session_user)
        #return user


class GetSearchSession(Resource):
    def render(self, request):
        sessionSearch = SessionManager(request).getSessionSearch()
        return json.dumps(sessionSearch)

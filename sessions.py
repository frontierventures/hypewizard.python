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
        sessionObject = ISessionObject(self.session)
        return sessionObject.user

    def setSessionUser(self, user):
        sessionObject = ISessionObject(self.session)
        sessionObject.user = user

    def clearSessionUser(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.user = {'id': 0, 'seed': 0, 'visit': 0, 'level': 1, 'currencyId': 0}
        print "%ssession_user cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionStore(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.store

    def setSessionStore(self, store):
        sessionObject = ISessionObject(self.session)
        sessionObject.store = store

    def clearSessionStore(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.store = {'id': 0}
        print "%ssessionStore cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionSearch(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.search

    def setSessionSearch(self, search):
        sessionObject = ISessionObject(self.session)
        sessionObject.search = search

    def clearSessionSearch(self):
        sessionObject = ISessionObject(self.session)
        seed = random.randint(0, sys.maxint)
        sessionObject.search = {'seed': seed, 'isTabOpen': False, 'query': '', 'sort': 'top', 'categoryId': '', 'index': 1}
        print "%ssessionSearch cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionProperty(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.propertyDict

    def setSessionProperty(self, propertyDict):
        sessionObject = ISessionObject(self.session)
        sessionObject.propertyDict = propertyDict

    def clearSessionProperty(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.propertyDict = {'id': 0}
        print "%ssessionProduct cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionOrder(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.order

    def setSessionOrder(self, order):
        sessionObject = ISessionObject(self.session)
        sessionObject.order = order

    def clearSessionOrder(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.order = {'id': 0}
        print "%ssessionOrder cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionTransaction(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.transaction

    def setSessionTransaction(self, transaction):
        sessionObject = ISessionObject(self.session)
        sessionObject.transaction = transaction

    def clearSessionTransaction(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.transaction = {'id': 0}
        print "%ssessionTransaction cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionReview(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.review

    def setSessionReview(self, review):
        sessionObject = ISessionObject(self.session)
        sessionObject.review = review

    def clearSessionReview(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.review = {'id': 0}
        print "%ssessionReview cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionAddress(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.address

    def setSessionAddress(self, address):
        sessionObject = ISessionObject(self.session)
        sessionObject.address = address

    def clearSessionAddress(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.address = {'id': 0}
        print "%ssessionAddress cleared%s" % (config.color.BLUE, config.color.ENDC)

    def getSessionResponse(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.response

    def setSessionResponse(self, response):
        sessionObject = ISessionObject(self.session)
        sessionObject.response = response

    def clearSessionResponse(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.response = {'class': 0, 'form': 0, 'text': ''}
        print "%ssession_response cleared%s" % (config.color.BLUE, config.color.ENDC)

    #LINK
    def getSessionLink(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.link

    def setSessionLink(self, link):
        sessionObject = ISessionObject(self.session)
        sessionObject.link = link

    def clearSessionLink(self):
        sessionObject = ISessionObject(self.session)
        sessionObject.link = {'id': 0}
        print "%ssessionLink cleared%s" % (config.color.BLUE, config.color.ENDC)

    def setSearchResults(self, searchResults):
        sessionObject = ISessionObject(self.session)
        sessionObject.searchResults = searchResults

    def getSearchResuls(self):
        sessionObject = ISessionObject(self.session)
        return sessionObject.searchResults


class ISessionObject(Interface):
    user = Attribute('')
    search = Attribute('')
    propertyDict = Attribute('')
    order = Attribute('')
    store = Attribute('')
    review = Attribute('')
    address = Attribute('')
    response = Attribute('')
    link = Attribute('')
    searchResults = Attribute('')


class SessionObject(object):
    implements(ISessionObject)

    def __init__(self, session):
        self.user = {'id': 0, 'level': 1, 'seed': 0, 'visit': 0, 'currencyId': 0}
        seed = random.randint(0, sys.maxint)
        self.search = {'seed': seed, 'isTabOpen': False, 'query': '', 'sort': 'top', 'categoryId': '', 'index': 1}
        self.propertyDict = {'id': 0}
        self.order = {'id': 0}
        self.store = {'id': 0}
        self.review = {'id': 0}
        self.address = {'id': 0}
        self.transaction = {'id': 0}
        self.link = {'id': 0}
        self.response = {'class': 0, 'form': 0, 'text': ''}
        self.searchResults = []


registerAdapter(SessionObject, Session, ISessionObject)


def disconnect(request, userId):
    buffer = set()
    for session in sessions:
        sessionObject = ISessionObject(session)
        session_user = sessionObject.user
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

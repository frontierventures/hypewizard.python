#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python .filepath import FilePath
#from parsley import makeGrammar
from twisted.web.template import XMLString, Element, renderer, tags

from data import db
from data import Profile
from sqlalchemy import func
from sessions import SessionManager

#import Image
import cgi
#import cloud
import elements
import config
import decimal
import definitions
#import descriptions
import error
import functions
import hashlib
import inspect
import itertools
import locale
import os

D = decimal.Decimal


class Login(Element):
    def __init__(self, session_user, session_response):
        self.session_user = session_user
        self.session_response = session_response
        self.loader = XMLString(FilePath('templates/forms/login.xml').getContent())

    @renderer
    def form(self, request, tag):
        session_user = self.session_user
        userEmail = ''
        if session_user.get('email'):
            userEmail = session_user['email']

        userPassword = ''
        if session_user.get('password'):
            userPassword = session_user['password']

        slots = {}
        slots['htmlEmail'] = userEmail
        slots['htmlPassword'] = userPassword
        yield tag.fillSlots(**slots)

    @renderer
    def alert(self, request, tag):
        session_response = self.session_response
        if session_response['text']:
            return elements.Alert(session_response)
        else:
            return []


class Register(Element):
    #print os.path.realpath(__file__)
    #loader = XMLString(FilePath('templates/forms/register.xml').getContent())
    loader = XMLString(FilePath(__file__).sibling('templates').child('forms').child('register.xml').getContent())

    def __init__(self, session_user, session_response):
        self.session_user = session_user
        self.session_response = session_response

    @renderer
    def form(self, request, tag):
        session_user = self.session_user

        email = ''
        if session_user.get('email'):
            email = session_user['email']

        new_password = ''
        if session_user.get('new_password'):
            new_password = session_user['new_password']

        new_password_repeat = ''
        if session_user.get('new_password_repeat'):
            new_password_repeat = session_user['new_password_repeat']

        bitcoin_address = ''
        if session_user.get('bitcoin_address'):
            bitcoin_address = session_user['bitcoin_address']

        twitter_name = ''
        if session_user.get('twitter_name'):
            twitter_name = session_user['twitter_name']

        slots = {}
        slots['email'] = email
        slots['new_password'] = new_password
        slots['new_password_repeat'] = new_password_repeat
        slots['bitcoin_address'] = bitcoin_address
        slots['twitter_name'] = twitter_name
        yield tag.fillSlots(**slots)

    @renderer
    def alert(self, request, tag):
        session_response = self.session_response
        if session_response['text']:
            return elements.Alert(session_response)
        else:
            return []

    @renderer
    def niche_option(self, request, tag):
        session_user = self.session_user

        #if session_user.get('niche'):
        #    niche = session_user['niche'] 

        for key in definitions.niches: 
            thisTagShouldBeSelected = False

            #if key == userCountry:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key
            slots['caption'] = definitions.niches[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python .filepath import FilePath
from parsley import makeGrammar
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
    loader = XMLString(FilePath('templates/forms/register.xml').getContent())

    def __init__(self, session_user, session_response):
        self.session_user = session_user
        self.session_response = session_response

    @renderer
    def form(self, request, tag):
        session_user = self.session_user

        email = ''
        if session_user.get('email'):
            email = session_user['email']

        password = ''
        if session_user.get('password'):
            password = session_user['password']

        repeat_password = ''
        if session_user.get('repeat_password'):
            repeat_password = session_user['repeat_password']

        bitcoin_address = ''
        if session_user.get('bitcoin_address'):
            bitcoin_address = session_user['bitcoin_address']

        twitter_name = ''
        if session_user.get('twitter_name'):
            bitcoin_address = session_user['twitter_name']

        slots = {}
        slots['htmlEmail'] = email
        slots['htmlPassword'] = password
        slots['htmlRepeatPassword'] = repeat_password
        slots['htmlBitcoinAddress'] = bitcoin_address
        slots['htmlTwitterName'] = twitter_name
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

#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python .filepath import FilePath
from parsley import makeGrammar
from twisted.web.template import XMLString, Element, renderer, tags

from data import db
from data import Profile, User
from sqlalchemy import func
from sessions import SessionManager

import activity
import cgi
import elements
import encryptor
import config
import decimal
import definitions
import error
#import explorer
#import receipt
#import report
import functions
import hashlib
import itertools
import login
import mailer
import os
import random
import sys

D = decimal.Decimal
Email = mailer.Email


# Post Actions


class Register(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../register', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'register'

        email = request.args.get('userEmail')[0]
        password = request.args.get('userPassword')[0]
        repeatPassword = request.args.get('userRepeatPassword')[0]
        bitcoinAddress = request.args.get('userBitcoinAddress')[0]
        country = request.args.get('userCountry')[0]

        session_user['email'] = email
        session_user['password'] = password
        session_user['repeatPassword'] = repeatPassword
        session_user['bitcoinAddress'] = repeatPassword
        session_user['country'] = country

        if error.email(request, email):
            return redirectTo('../register', request)

        users = db.query(User).filter(User.status == 'active')
        user = users.filter(User.email == email).first()

        if user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[3]})
            return redirectTo('../register', request)

        if error.password(request, password):
            return redirectTo('../register', request)

        if error.repeatPassword(request, repeatPassword):
            return redirectTo('../register', request)

        if error.mismatchPassword(request, password, repeatPassword):
            return redirectTo('../register', request)

        if error.bitcoinAddress(request, bitcoinAddress):
            return redirectTo('../register', request)

        if not request.args.get('isTermsChecked'):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
            return redirectTo('../register', request)

        if request.args.get('button')[0] == 'Register':
            timestamp = config.create_timestamp()
            token = hashlib.sha224(str(email)).hexdigest()
            password = encryptor.hashPassword(password)
            seed = random.randint(0, sys.maxint)

            data = {
                'status': 'unverified',
                'type': 2,
                'loginTimestamp': timestamp,
                'email': email,
                'password': password,
                'isEmailVerified': 0,
                'ip': ''
                }

            newUser = User(data)
            data = {            
                'created_at': timestamp,
                'updateTimestamp': timestamp,
                'first': '',
                'last': '',
                'token': token,
                'bitcoinAddress': bitcoinAddress,
                'country': country,
                'seed': seed,
                'balance': 0, 
                'unreadMessages': 0
                }
            newProfile = Profile(data)

            newUser.profiles = [newProfile]

            db.add(newUser)
            db.commit()

            url = 'http://www.sptrust.co/verifyEmail?id=%s&token=%s' % (str(newUser.id), token)

            plain = mailer.verificationPlain(url)
            html = mailer.verificationHtml(url)
            Email(mailer.noreply, email, 'Getting Started', plain, html).send()

            email = str(email)
            activity.pushToSocket(self.echoFactory, '%s**** registered' % email[0])
            activity.pushToDatabase('%s registered' % email)

            url = login.make_session(request, new_user.id)
            return redirectTo(url, request)

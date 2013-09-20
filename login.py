#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from data import Profile, User
from data import db
from sessions import SessionManager

import activity
import elements
import config
import definitions
import functions
import encryptor
import error
import json
import actions
import mailer
import pages
import random
import re
import string

Email = mailer.Email


def assemble(root):
    root.putChild('login', Main())
    root.putChild('authenticate', Authenticate())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'login'

        if session_user['id'] >= 1:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()
        if request.args.get('verify'):
            verify = request.args.get('verify')[0]
            if verify == 'ok':
                session_response = {'class': 2, 'form': 0, 'text': definitions.VERIFY_SUCCESS}

        Page = pages.Login('Smart Property Group - Login', 'login')
        Page.session_user = session_user
        Page.session_response = session_response

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.YELLOW, session_response, config.color.ENDC)
        SessionManager(request).clearSessionResponse()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Authenticate(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'login'

        email = request.args.get('email')[0]
        password = request.args.get('password')[0]

        session_user['email'] = email
        session_user['password'] = password

        if error.email(request, email):
            return redirectTo('../login', request)

        if error.password(request, password):
            return redirectTo('../login', request)

        users = db.query(User).filter(User.email == email)
        user = users.filter(User.status != 'deleted').first()

        if not user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[2]})
            return redirectTo('../login', request)
        
        if not encryptor.check_password(user.password, password):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD[2]})
            return redirectTo('../login', request)

        if request.args.get('button')[0] == 'Login':
            activity.push_to_database(user.id, session_user['action'], '')
            url = make_session(request, user.id)
            return redirectTo(url, request)


class RecoverPassword(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['userEmail'] = request.args.get('userEmail')[0]
        #SessionManager(request).setSessionUser(session_user)

        userEmail = session_user['userEmail']
        #request.setSessionResponseCode(200)

        if not userEmail:
            return json.dumps(dict(response=0, text=definitions.EMAIL[0]))
        elif not re.match(definitions.REGEX_EMAIL, userEmail):
            return json.dumps(dict(response=0, text=definitions.EMAIL[1]))

        user = db.query(User).filter(User.email == userEmail).first()
        if not user:
            return json.dumps(dict(response=0, text=definitions.EMAIL[2]))

        password = ''.join(random.sample(string.digits, 5))
        user.password = encryptor.hashPassword(password)
        db.commit()

        plain = mailer.passwordRecoveryPlain(userEmail, password)
        html = mailer.passwordRecoveryHtml(userEmail, password)
        Email(mailer.noreply, userEmail, 'Your  password was reset!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.PASSWORD[3]))


def make_session(request, user_id):
    SessionManager(request).add()

    user = db.query(User).filter(User.id == user_id).first()
    user.login_timestamp = config.create_timestamp()
    user.ip = request.getClientIP()
    db.commit()

    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    session_user = SessionManager(request).get_session_user()
    session_user['id'] = user.id
    session_user['level'] = user.level
    session_user['ip'] = user.ip
    session_user['login_timestamp'] = user.login_timestamp
    session_user['status'] = user.status 
    session_user['is_email_verified'] = user.is_email_verified
    session_user['balance'] = profile.balance
    session_user['twitter_name'] = profile.twitter_name
    session_user['bitcoin_address'] = profile.bitcoin_address

    url = '../'
    if user.level in [1]:
        url = '../'

    #if user.status == 'verified':
    #    url = '../settings'

    #if user.status == 'unverified':
    #    url = '../settings'

    if user.level == 0:
        url = '../summary_users'
    
    return url

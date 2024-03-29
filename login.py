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
    root.putChild('reset_password', Reset())
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

        Page = pages.Login('%s Login' % config.company_name, 'login')
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

        response = error.email(request, email)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../login', request)

        response = error.new_password(request, password)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
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


class Reset(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['email'] = request.args.get('email')[0]
        #SessionManager(request).setSessionUser(session_user)

        email = session_user['email']
        #request.setSessionResponseCode(200)

        response = {}
        response['error'] = True

        if not email:
            response['message'] = definitions.EMAIL[0]
            return json.dumps(response)
        elif not re.match(definitions.REGEX_EMAIL, email):
            response['message'] = definitions.EMAIL[1]
            return json.dumps(response)

        user = db.query(User).filter(User.email == email).first()
        if not user:
            response['message'] = definitions.EMAIL[2]
            return json.dumps(response)

        password = ''.join(random.sample(string.digits, 5))
        user.password = encryptor.hash_password(password)
        db.commit()

        plain = mailer.password_reset_memo_plain(user.email, password)
        html = mailer.password_reset_memo_html(user.email, password)
        Email(mailer.noreply, user.email, 'Your Hype Wizard password was reset!', plain, html).send()

        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = '../' 

        return json.dumps(response) 


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
    session_user['available_balance'] = profile.available_balance
    session_user['reserved_balance'] = profile.reserved_balance
    session_user['twitter_name'] = profile.twitter_name
    session_user['twitter_id'] = profile.twitter_id
    session_user['bitcoin_address'] = profile.bitcoin_address
    session_user['transaction_count'] = profile.transaction_count
    session_user['offer_count'] = profile.offer_count

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

#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import flattenString
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User
from data import db
from sessions import SessionManager

import activity
import config
import definitions
import encryptor
import error
import hashlib
import login
import mailer
import pages
import random
import sys

Email = mailer.Email


def assemble(root):
    root.putChild('create_user', Create())
    root.putChild('register', Main())
    root.putChild('resend_token', Resend())
    root.putChild('verify_ownership', Verify())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'register'

        if session_user['id'] >= 1:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        Page = pages.Register('%s Register' % config.company_name, 'register')
        Page.session_user = session_user
        Page.session_response = session_response

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.YELLOW, session_response, config.color.ENDC)

        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Create(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../register', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'register'

        email = request.args.get('email')[0]
        password = request.args.get('password')[0]
        repeat_password = request.args.get('repeat_password')[0]
        bitcoin_address = request.args.get('bitcoin_address')[0]
        twitter_name = request.args.get('twitter_name')[0]
        niche = request.args.get('niche')[0]

        session_user['email'] = email
        session_user['password'] = password
        session_user['repeatPassword'] = repeat_password
        session_user['bitcoinAddress'] = bitcoin_address
        session_user['twitter_name'] = twitter_name
        session_user['niche'] = niche

        if error.email(request, email):
            return redirectTo('../register', request)

        users = db.query(User).filter(User.status == 'active')
        user = users.filter(User.email == email).first()

        if user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[3]})
            return redirectTo('../register', request)

        if error.password(request, password):
            return redirectTo('../register', request)

        if error.repeatPassword(request, repeat_password):
            return redirectTo('../register', request)

        if error.mismatchPassword(request, password, repeat_password):
            return redirectTo('../register', request)

        if error.bitcoinAddress(request, bitcoin_address):
            return redirectTo('../register', request)

        if not request.args.get('is_terms_accepted'):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
            return redirectTo('../register', request)

        if request.args.get('button')[0] == 'Register':
            timestamp = config.create_timestamp()
            token = hashlib.sha224(str(email)).hexdigest()
            password = encryptor.hash_password(password)
            seed = random.randint(0, sys.maxint)

            data = {
                'status': 'unverified',
                'level': 1,
                'login_timestamp': timestamp,
                'email': email,
                'password': password,
                'is_email_verified': False,
                'ip': ''
                }

            new_user = User(data)
            data = {            
                'created_at': timestamp,
                'updated_at': timestamp,
                'first': '',
                'last': '',
                'token': token,
                'bitcoin_address': bitcoin_address,
                'available_balance': 0,
                'reserved_balance': 0,
                'twitter_name': twitter_name,
                'niche': niche,
                'transaction_count': 0,
                'offer_count': 0
                }
            new_profile = Profile(data)

            new_user.profiles = [new_profile]

            db.add(new_user)
            db.commit()

            url = 'http://www.hypewhiz.com/verify_email?id=%s&token=%s' % (str(new_user.id), token)

            plain = mailer.verificationPlain(url)
            html = mailer.verificationHtml(url)
            Email(mailer.noreply, email, 'Getting Started with Hype Wizard', plain, html).send()

            #activity.push_to_socket(self.echoFactory, '%s**** registered' % email[0])
            activity.push_to_database(new_user.id, session_user['action'], '')

            url = login.make_session(request, new_user.id)
            return redirectTo(url, request)


class Verify(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        try:
            user_id = int(request.args.get('id')[0])
        except:
            return redirectTo('../', request)

        try:
            token = request.args.get('token')[0]
        except:
            return redirectTo('../', request)

        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            return redirectTo('../', request)

        if profile.token == token:
            user = db.query(User).filter(User.id == user_id).first()
            user.status = 'verified' 
            profile.token = ''
            db.commit()

            sessions.disconnect(request, userId)
            SessionManager(request).setSessionResponse({'class': 2, 'form': 0, 'text': definitions.VERIFY_SUCCESS})
            return redirectTo('../login?verify=ok', request)
        else:
            return redirectTo('../', request)


class Resend(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        userId = sessionUser['id']

        user = db.query(User).filter(User.id == user_id).first()
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()

        url = 'http://www.coingig.com/verify_ownership?id=%s&token=%s' % (str(user_id), profile.token)
        plain = mailer.verificationPlain(url)
        html = mailer.verificationHtml(url)
        Email(mailer.noreply, user.email, 'Getting Started with Hype Wizard', plain, html).send()

        #SessionManager(request).setSessionResponse({'class': 2, 'form': 0, 'text': definitions.UNDEF})
        return redirectTo('../', request)

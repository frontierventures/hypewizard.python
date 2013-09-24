#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import flattenString
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, TwitterUserData, User
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
import sessions
import sys
import twitter_api

Email = mailer.Email


def assemble(root):
    root.putChild('create_user', Create())
    root.putChild('register', Main())
    root.putChild('verify_email', Verify())
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
        new_password = request.args.get('new_password')[0]
        new_password_repeat = request.args.get('new_password_repeat')[0]
        bitcoin_address = request.args.get('bitcoin_address')[0]
        twitter_name = request.args.get('twitter_name')[0]
        niche = request.args.get('niche')[0]

        session_user['email'] = email
        session_user['new_password'] = new_password
        session_user['new_password_repeat'] = new_password_repeat
        session_user['bitcoin_address'] = bitcoin_address
        session_user['twitter_name'] = twitter_name
        session_user['niche'] = niche

        response = error.email(request, email)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        users = db.query(User).filter(User.status == 'active')
        user = users.filter(User.email == email).first()

        if user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[3]})
            return redirectTo('../register', request)

        response = error.new_password(request, new_password)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        response = error.new_password_repeat(request, new_password_repeat)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        response = error.password_match(request, new_password, new_password_repeat)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        response = error.bitcoin_address(request, bitcoin_address)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        response = error.twitter_name(request, twitter_name)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        twitter_user_data = db.query(TwitterUserData).filter(TwitterUserData.twitter_name == twitter_name).first()
        if twitter_user_data:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': 'Twitter name already used'})
            return redirectTo('../register', request)

        response = twitter_api.get_user(twitter_name)
        if response['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': response['message']})
            return redirectTo('../register', request)

        twitter_user = response['user']

        if not request.args.get('is_terms_accepted'):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
            return redirectTo('../register', request)

        if request.args.get('button')[0] == 'Register':
            timestamp = config.create_timestamp()
            token = hashlib.sha224(str(email)).hexdigest()
            password = encryptor.hash_password(new_password)
            seed = random.randint(0, sys.maxint)

            data = {
                'status': 'active',
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
                'token': token,
                'bitcoin_address': bitcoin_address,
                'available_balance': 0,
                'reserved_balance': 0,
                'twitter_name': twitter_name,
                'twitter_id': twitter_user.id,
                'niche': niche,
                'transaction_count': 0,
                'offer_count': 0
                }
            new_profile = Profile(data)

            new_user.profiles = [new_profile]

            data = {            
                'twitter_id': twitter_user.id,
                'twitter_name': twitter_name,
                'twitter_image': twitter_user.profile_image_url,
            }
            new_twitter_user = TwitterUserData(data)
            new_user.twitter_user_data = [new_twitter_user]

            db.add(new_user)
            db.commit()

            url = '%s/verify_email?id=%s&token=%s' % (config.company_url, str(new_user.id), token)

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
            user.is_email_verified = True
            profile.token = ''
            db.commit()

            sessions.disconnect(request, userId)
            SessionManager(request).setSessionResponse({'class': 2, 'form': 0, 'text': definitions.VERIFY_SUCCESS})
            return redirectTo('../login?verify=ok', request)
        else:
            return redirectTo('../', request)

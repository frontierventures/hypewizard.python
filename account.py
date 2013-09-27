#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString


import twitter_api
import config
import definitions
import encryptor
import error
import json
import locale
import mailer
import pages

from data import db
from sqlalchemy.sql import and_
from data import Profile, TwitterUserData, User
from sessions import SessionManager

Email = mailer.Email


def assemble(root):
    root.putChild('account', Main())
    root.putChild('change_password', Change())
    root.putChild('resend_token', Resend())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'account'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        Page = pages.Account('%s Account' % config.company_name, 'account')
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Details(Element):
    def __init__(self, session_user):
        self.session_user = session_user

        self.profile = db.query(Profile).filter(Profile.id == session_user['id']).first()

        if session_user['is_email_verified']:
            template = 'templates/elements/verified_account.xml'
        else:
            template = 'templates/elements/unverified_account.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.twitter_user = twitter_api.get_user(twitter_id=self.session_user['twitter_id'])['user']
          

        self.twitter_user_data = db.query(TwitterUserData).filter(TwitterUserData.twitter_id == self.session_user['twitter_id']).first()

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['name'] = str(self.twitter_user.name)
        slots['created_at'] = str(self.twitter_user.created_at)
        slots['statuses_count'] = str(self.twitter_user.statuses_count)
        slots['followers_count'] = str(self.twitter_user.followers_count)
        slots['twitter_image'] = str(self.twitter_user_data.image)
        slots['available_balance'] = str(self.profile.available_balance)
        slots['reserved_balance'] = str(self.profile.reserved_balance)
        slots['market_score'] = str(0)
        #slots['status_text'] = status.text.encode('utf-8')
        yield tag.clone().fillSlots(**slots)


class Change(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'change_password'

        old_password = request.args.get('old_password')[0]
        new_password = request.args.get('new_password')[0]
        new_password_repeat = request.args.get('new_password_repeat')[0]

        session_user['old_password'] = old_password
        session_user['new_password'] = new_password
        session_user['new_password_repeat'] = new_password_repeat

        response = error.old_password(request, old_password)
        if response['error']:
            return json.dumps(response) 

        response = error.new_password(request, new_password)
        if response['error']:
            return json.dumps(response) 

        response = error.new_password_repeat(request, new_password_repeat)
        if response['error']:
            return json.dumps(response) 

        response = error.password_match(request, new_password, new_password_repeat)
        if response['error']:
            return json.dumps(response) 

        user = db.query(User).filter(User.id == session_user['id']).first()

        user.password = encryptor.hash_password(new_password)
        db.commit()

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = '../account' 

        return json.dumps(response) 


class Resend(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()

        user = db.query(User).filter(User.id == session_user['id']).first()
        profile = db.query(Profile).filter(Profile.user_id == session_user['id']).first()

        url = '%s/verify_email?id=%s&token=%s' % (config.company_url, str(session_user['id']), token)

        plain = mailer.verify_email_memo_plain(url)
        html = mailer.verify_email_memo_html(url)
        Email(mailer.noreply, user.email, 'Instructions to verify your Hype Wizard email', plain, html).send()


        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = '../account'

        return json.dumps(response) 

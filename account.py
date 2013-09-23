#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from sessions import SessionManager

import twitter_api
import config
import locale
import pages

from data import db
from sqlalchemy.sql import and_
from data import Profile
from sessions import SessionManager


def assemble(root):
    root.putChild('account', Main())
    root.putChild('change_password', Change())
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

        if session_user['status'] == 'verified':
            template = 'templates/elements/verified_account.xml'
        else:
            template = 'templates/elements/unverified_account.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.twitter_user = twitter_api.get_user_by_id(self.session_user['twitter_id'])

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['name'] = str(self.twitter_user.name)
        slots['created_at'] = str(self.twitter_user.created_at)
        slots['statuses_count'] = str(self.twitter_user.statuses_count)
        slots['followers_count'] = str(self.twitter_user.followers_count)
        slots['market_score'] = str(0)
        #slots['status_text'] = status.text.encode('utf-8')
        yield tag.clone().fillSlots(**slots)


class Change(Resource):
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

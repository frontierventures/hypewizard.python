#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User 
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages


def assemble(root):
    root.putChild('summary_users', Main())
    #root.putChild('process_user', Process())
    #root.putChild('approve_user', Approve())
    #root.putChild('disapprove_user', Disapprove())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'summary_users'

        if session_user['level'] != 0:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'active'

        Page = pages.Offers('%s Summary Users' % config.company_name, 'summary_users', filters)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.BLUE, session_response, config.color.ENDC)

        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Table(Element):
    def __init__(self, session_user, filters):
        self.session_user = session_user
        self.filters = filters

        users = db.query(User)

        if filters['status'] == 'active':
            users = users.filter(User.status.in_(['active', 'approved'])).order_by(User.updated_at.desc())

        if filters['status'] == '':
            users = users.filter(User.status == 'complete').order_by(User.updated_at.desc())

        if users.count() == 0:
            template = 'templates/elements/empty_summary_users_table.xml'
        else:
            template = 'templates/elements/summary_users_table.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.users = users

    @renderer
    def count(self, request, tag):
        statuses = {
            'open': 'Open',
            'complete': 'Complete'
        }

        slots = {}
        slots['user_status'] = statuses[self.filters['status']]
        slots['user_count'] = str(self.users.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def user_status(self, request, tag):
        statuses = {
            'active': 'Active',
            'deleted': 'Deleted'
        }

        for key in statuses:
            thisTagShouldBeSelected = False

            if key == self.filters['status']:
                thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key
            slots['caption'] = statuses[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def row(self, request, tag):
        for user in self.users:
            user = twitter_api.get_user(user.promoter_twitter_name)
            slots = {}
            slots['status'] = user.status 
            slots['created_at'] = config.convert_timestamp(user.created_at, config.STANDARD)
            slots['updated_at'] = config.convert_timestamp(user.updated_at, config.STANDARD)
            slots['user_id'] = str(user.id)
            slots['email'] = str(user.email)
            self.user = user
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []

        if self.user.status == 'open':
            buttons.append({
                'url': '../process_user?action=approve&id=%s' % self.user.id,
                'caption': 'Approve' 
            })
            buttons.append({
                'url': '../process_user?action=disapprove&id=%s' % self.user.id,
                'caption': 'Disapprove' 
            })

        for button in buttons:
            slots = {}
            slots = {}
            slots['caption'] = button['caption']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 


class Process(Resource):
    def render(self, request):
        session_user = SessionManager(request).get_session_user()

        response = {'error': True}
        try:
            action = request.args.get('action')[0]
        except:
            return redirectTo('../', request)

        try:
            user_id = int(request.args.get('id')[0])
        except:
            return redirectTo('../', request)

        response['error'] = False
        response['action'] = action

        response['user'] = {
                'id': str(user_id)
            } 

        return json.dumps(response)


class Approve(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'approve_user'

        try:
            user_id = int(request.args.get('user_id')[0])
        except:
            return redirectTo('../users', request)

        user = db.query(Transaction).filter(Transaction.id == user_id).first()

        if user.client_id != session_user['id']:
            return redirectTo('../', request)

        is_confirmed = request.args.get('is_confirmed')[0]
        if is_confirmed == 'no':
            return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

        timestamp = config.create_timestamp()
        
        #ask = db.query(Ask).filter(Ask.id == ).first()

        user.updated_at = timestamp 
        user.status = 'approved'
        db.commit()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))


class Disapprove(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'disapprove'

        try:
            user_id = int(request.args.get('user_id')[0])
        except:
            return redirectTo('../users', request)

        user = db.query(Transaction).filter(Transaction.id == user_id).first()

        if user.client_id != session_user['id']:
            return redirectTo('../', request)

        is_confirmed = request.args.get('is_confirmed')[0]
        if is_confirmed == 'no':
            return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

        timestamp = config.create_timestamp()
        
        user.updated_at = timestamp 
        user.status = 'cancelled'

        client = db.query(Profile).filter(Profile.user_id == user.client_id).first()
        client.user_count -= 1
        client.available_balance += user.charge
        client.reserved_balance -= user.charge

        promoter = db.query(Profile).filter(Profile.user_id == user.promoter_id).first()
        promoter.transaction_count -= 1
        
        db.commit()
        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

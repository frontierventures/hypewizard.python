#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Transaction, Profile, User 
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages


def assemble(root):
    root.putChild('summary_transactions', Main())
    #root.putChild('process_user', Process())
    #root.putChild('approve_user', Approve())
    #root.putChild('disapprove_user', Disapprove())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'summary_transactions'

        if session_user['level'] != 0:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'open'

        Page = pages.SummaryTransactions('%s Summary Transactions' % config.company_name, 'summary_transactions', filters)
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

        transactions = db.query(Transaction)

        if filters['status'] == 'open':
            transactions = transactions.filter(Transaction.status.in_(['open', 'approved'])).order_by(Transaction.created_at.desc())

        if filters['status'] == 'complete':
            transactions = transactions.filter(Transaction.status == 'complete').order_by(Transaction.created_at.desc())

        if transactions.count() == 0:
            template = 'templates/elements/empty_summary_transactions_table.xml'
        else:
            template = 'templates/elements/summary_transactions_table.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.transactions = transactions

    @renderer
    def count(self, request, tag):
        statuses = {
            'open': 'Open',
            'complete': 'Complete'
        }

        slots = {}
        slots['transaction_status'] = statuses[self.filters['status']]
        slots['transaction_count'] = str(self.transactions.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def transaction_status(self, request, tag):
        statuses = {
            'open': 'Open',
            'complete': 'Complete'
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
        for transaction in self.transactions:
            slots = {}
            slots['status'] = transaction.status 
            slots['created_at'] = config.convert_timestamp(transaction.created_at, config.STANDARD)
            slots['transaction_id'] = str(transaction.id)
            self.transaction = transaction
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []

        if self.transaction.status == 'open':
            buttons.append({
                'url': '../process_transaction?action=approve&id=%s' % self.transaction.id,
                'caption': 'Approve' 
            })
            buttons.append({
                'url': '../process_transaction?action=disapprove&id=%s' % self.transaction.id,
                'caption': 'Disapprove' 
            })

        for button in buttons:
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
        
        #transaction = db.query(Transaction).filter(Transaction.id == ).first()

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

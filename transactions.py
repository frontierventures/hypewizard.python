#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Ask, Bid, Profile, Transaction
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages
import twitter_api


def assemble(root):
    root.putChild('transactions', Main())
    root.putChild('create_transaction', Create())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'transactions'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'open'

        try:
            filters['kind'] = request.args.get('kind')[0]
        except:
            filters['kind'] = 'promoter'

        Page = pages.Transactions('Transactions', 'transactions', filters)
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

        if filters['kind'] == 'promoter':
            transactions = db.query(Transaction).filter(Transaction.promoter_id == session_user['id'])
        
        if filters['kind'] == 'client':
            transactions = db.query(Transaction).filter(Transaction.client_id == session_user['id'])

        if filters['status'] == 'open':
            transactions = transactions.filter(Transaction.status == 'open').order_by(Transaction.update_timestamp.desc())
        if filters['status'] == 'complete':
            transactions = transactions.filter(Transaction.status == 'complete').order_by(Transaction.update_timestamp.desc())

        if transactions.count() == 0:
            template = 'templates/elements/no_transactions_table.xml'
        else:
            template = 'templates/elements/transactions_table.xml'

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
            slots['create_timestamp'] = config.convert_timestamp(transaction.create_timestamp, config.STANDARD)
            slots['transaction_id'] = str(transaction.id)
            slots['promoter_twitter_name'] = transaction.promoter_twitter_name.encode('utf-8')
            slots['promoter_twitter_name_url'] = 'http://www.twitter.com/%s' % transaction.promoter_twitter_name
            slots['twitter_status_id'] = str(transaction.twitter_status_id) 
            slots['twitter_status_id_url'] = 'http://www.twitter.com/%s/status/%s' % (transaction.promoter_twitter_name, transaction.twitter_status_id)
            slots['charge'] = str(transaction.charge) 
            self.transaction = transaction
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []

        buttons.append({
            'url': '../process_transaction?action=claim&id=%s' % self.transaction.id,
            'caption': 'Claim Funds' 
        })

        for button in buttons:
            slots = {}
            slots = {}
            slots['caption'] = button['caption']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 


class Create(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'create_transaction'

        print "HERE" * 20
        
        try:
            transaction_type = request.args.get('transaction_type')[0]
        except:
            return redirectTo('../', request)

        timestamp = config.create_timestamp()
        #####################################
        # Engage Client
        #####################################
        if transaction_type == 'engage_client':
            is_confirmed = request.args.get('is_confirmed')[0]
            if is_confirmed == 'no':
                return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))
           
            try:
                ask_id = int(request.args.get('ask_id')[0])
            except:
                return redirectTo('../', request)
            
            ask = db.query(Ask).filter(Ask.id == ask_id).first()

            data = {
                'status': 'open',
                'create_timestamp': timestamp,
                'update_timestamp': timestamp,
                'client_twitter_name': ask.twitter_name,
                'promoter_twitter_name': session_user['twitter_name'],
                'twitter_status_id': ask.twitter_status_id,
                'client_id': ask.user_id,
                'promoter_id': session_user['id'],
                'charge': ask.cost 
            }
        
        #####################################
        # Engage Promoter
        #####################################
        if transaction_type == 'engage_promoter':
            twitter_status_id = request.args.get('twitter_status_id')[0]
            try:
                bid_id = int(request.args.get('bid_id')[0])
            except:
                return redirectTo('../', request)
            
            bid = db.query(Bid).filter(Bid.id == bid_id).first()

            data = {
                'status': 'open',
                'create_timestamp': timestamp,
                'update_timestamp': timestamp,
                'client_twitter_name': session_user['twitter_name'],
                'promoter_twitter_name': bid.twitter_name,
                'twitter_status_id': twitter_status_id,
                'client_id': session_user['id'],
                'promoter_id': bid.user_id,
                'charge': bid.cost 
            }

        #try:
        #    bid_id = int(request.args.get('bid_id')[0])
        #except:
        #    return redirectTo('../', request)

        #twitter_status_id = request.args.get('twitter_status_id')[0]

        #bid = db.query(Bid).filter(Bid.id == bid_id).first()

        #data = {
        #    'status': 'open',
        #    'create_timestamp': timestamp,
        #    'update_timestamp': timestamp,
        #    'client_twitter_name': session_user['twitter_name'],
        #    'promoter_twitter_name': bid.twitter_name,
        #    'twitter_status_id': twitter_status_id,
        #    'client_id': session_user['id'],
        #    'promoter_id': bid.seller_id,
        #    'charge': bid.cost 
        #}


        new_transaction = Transaction(data)
        db.add(new_transaction)

        profile = db.query(Profile).filter(Profile.user_id == session_user['id']).first()
        profile.transaction_count += 1

        session_user['transaction_count'] += 1

        db.commit()

        #plain = mailer.offerMemoPlain(seller)
        #html = mailer.offerMemoHtml(seller)
        #Email(mailer.noreply, seller_email, 'You have a new offer at Coingig.com!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

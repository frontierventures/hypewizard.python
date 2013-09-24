#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Ask, Bid, Profile, Offer, Transaction, TwitterUserData, User
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import mailer
import pages
import time
import twitter_api

Email = mailer.Email


def assemble(root):
    root.putChild('transactions', Main())
    root.putChild('create_transaction', Create())
    root.putChild('process_transaction', Process())
    root.putChild('complete_transaction', Complete())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'transactions'

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

        Page = pages.Transactions('%s Transactions' % config.company_name, 'transactions', filters)
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

        transactions = db.query(Transaction).filter(Transaction.promoter_id == session_user['id'])
        
        if filters['status'] == 'open':
            transactions = transactions.filter(Transaction.status.in_(['open', 'approved'])).order_by(Transaction.updated_at.desc())
        if filters['status'] == 'complete':
            transactions = transactions.filter(Transaction.status == 'complete').order_by(Transaction.updated_at.desc())

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
        for index, transaction in enumerate(self.transactions):
            slots = {}
            slots['row_id'] = 'row_%s' % index
            slots['status'] = transaction.status 
            slots['created_at'] = config.convert_timestamp(transaction.created_at, config.STANDARD)
            slots['updated_at'] = config.convert_timestamp(transaction.updated_at, config.STANDARD)
            slots['transaction_id'] = str(transaction.id)
            
            item = db.query(TwitterUserData).filter(TwitterUserData.twitter_id == transaction.client_twitter_id).first()
            slots['client_twitter_name'] = item.twitter_name.encode('utf-8')

            slots['client_twitter_name_url'] = 'http://www.twitter.com/%s' % item.twitter_name
            slots['twitter_status_id'] = str(transaction.twitter_status_id) 
            slots['twitter_status_id_url'] = 'http://www.twitter.com/%s/status/%s' % (item.twitter_name, transaction.twitter_status_id)
            slots['charge'] = str(transaction.charge) 
            self.transaction = transaction
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []
        
        if self.transaction.status == 'approved':
            buttons.append({
                'url': '../process_transaction?action=claim&id=%s' % self.transaction.id,
                'caption': 'Claim Balance' 
            })

        for button in buttons:
            slots = {}
            slots = {}
            slots['caption'] = button['caption']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 


class Process(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'process_transaction'

        response = {'error': True}
        try:
            action = request.args.get('action')[0]
        except:
            return redirectTo('../', request)

        if action == 'claim':
            try:
                transaction_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../transactions', request)

            response['error'] = False
            response['action'] = action

            response['transaction'] = {
                    'id': str(transaction_id)
                } 

            return json.dumps(response)


class Create(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'create_transaction'

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

            charge = ask.cost

            data = {
                'status': 'open',
                'kind': 'client-first',
                'created_at': timestamp,
                'updated_at': timestamp,
                'client_twitter_id': ask.twitter_id,
                'promoter_twitter_id': session_user['twitter_id'],
                'twitter_status_id': ask.twitter_status_id,
                'client_id': ask.user_id,
                'promoter_id': session_user['id'],
                'charge': charge, 
                'ask_id': ask_id,
                'bid_id': 0
            }

            new_transaction = Transaction(data)
            db.add(new_transaction)

            promoter = db.query(Profile).filter(Profile.user_id == session_user['id']).first()
            promoter.transaction_count += 1

            client = db.query(Profile).filter(Profile.user_id == ask.user_id).first()
            client.offer_count += 1 

            db.commit()

            client = db.query(User).filter(User.id == client.user_id).first()

            plain = mailer.offer_created_memo_plain(promoter, new_transaction)
            html = mailer.offer_created_memo_html(promoter, new_transaction)
            Email(mailer.noreply, client.email, 'You have a new Hype Wizard promotional offer pending!', plain, html).send()

            url = '../transactions'
        
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

            charge = bid.cost

            client = db.query(Profile).filter(Profile.user_id == session_user['id']).first()
            if client.available_balance < charge: 
                response = {}
                response['error'] = True
                response['message'] = "This promoter charges %s per retweet." % charge 
                return json.dumps(response) 

            #asks = db.query(Ask).filter(Ask.twitter_status_id == twitter_status_id)
            #ask = asks.filter(Ask.status == 'active').first()

            transactions = db.query(Transaction).filter(Transaction.client_id == session_user['id'])
            transactions = transactions.filter(Transaction.status.in_(['open', 'approved']))  
            transaction = transactions.filter(Transaction.twitter_status_id == twitter_status_id).first()

            if transaction:
                response = {}
                response['error'] = True
                response['message'] = 'You already seeking to promoter this tweet with this promoter.' 
                return json.dumps(response) 

            data = {
                'status': 'approved',
                'kind': 'direct',
                'created_at': timestamp,
                'updated_at': timestamp,
                'client_twitter_id': session_user['twitter_id'],
                'promoter_twitter_id': bid.twitter_id,
                'twitter_status_id': twitter_status_id,
                'client_id': session_user['id'],
                'promoter_id': bid.user_id,
                'charge': charge,
                'ask_id': 0,
                'bid_id': bid_id
            }

            new_transaction = Transaction(data)
            db.add(new_transaction)

            promoter = db.query(Profile).filter(Profile.user_id == bid.user_id).first()
            promoter.transaction_count += 1

            client.offer_count += 1 
            client.available_balance -= charge
            client.reserved_balance += charge

            db.commit()

            promoter = db.query(User).filter(User.id == promoter.user_id).first()

            plain = mailer.promotion_request_memo_plain()
            html = mailer.promotion_request_memo_html()

            Email(mailer.noreply, promoter.email, 'Your have a request with Hype Wizard!', plain, html).send()

            url = '../offers'

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = url 
        return json.dumps(response) 


class Complete(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        
        time.sleep(2)
        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'complete_transaction'

        is_confirmed = request.args.get('is_confirmed')[0]
        if is_confirmed == 'no':
            response = {}
            response['error'] = False
            response['message'] = definitions.MESSAGE_SUCCESS
            response['url'] = '../transactions'
            return json.dumps(response) 
        
        try:
            transaction_id = int(request.args.get('transaction_id')[0])
        except:
            return redirectTo('../', request)
        
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

        if transaction.promoter_id != session_user['id']:
            return redirectTo('../', request)

        #####################################
        # Check Retweet Maturity
        #####################################
        
        response = twitter_api.get_retweet_duration(transaction.promoter_twitter_id, transaction.twitter_status_id)
        if response['error']:
            response = {}
            response['error'] = True
            response['message'] = 'Twitter Api error'
            return json.dumps(response) 
        else:
            if response['is_retweet_found']:
                delta = response['delta']
                if delta < 86400:
                    print delta * 20
                    timestamp = time.strftime('%H hrs %M mins %S secs', time.gmtime(delta))
                    response = {}
                    response['error'] = True
                    response['message'] = 'Please wait until the end of promotion period (ETA: %s)' % timestamp 
                    return json.dumps(response) 
            else:
                response = {}
                response['error'] = True
                response['message'] = 'Please retweet for your client'
                return json.dumps(response) 

        #####################################

        timestamp = config.create_timestamp()
        
        transaction.updated_at = timestamp 
        transaction.status = 'complete'

        client = db.query(Profile).filter(Profile.user_id == transaction.client_id).first()
        client.offer_count -= 1
        client.reserved_balance -= transaction.charge

        promoter = db.query(Profile).filter(Profile.user_id == transaction.promoter_id).first()
        promoter.transaction_count -= 1
        promoter.available_balance += transaction.charge

        if transaction.ask_id != 0:
            ask = db.query(Ask).filter(Ask.id == transaction.ask_id).first()
            ask.target += 1

            if ask.target == ask.goal:
                ask.status = 'withdrawn'

        if transaction.bid_id != 0:
            bid = db.query(Bid).filter(Bid.id == transaction.bid_id).first()
            bid.tally += 1

        db.commit()

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = '../transactions'

        return json.dumps(response) 

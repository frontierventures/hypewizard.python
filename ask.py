#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Ask, Profile, User
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages
import twitter_api


def assemble(root):
    root.putChild('ask', Main())
    root.putChild('process_ask', Process())
    root.putChild('create_ask', Create())
    root.putChild('withdraw_ask', Withdraw())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_response = SessionManager(request).get_session_response()
        
        if session_user['id'] == 0:
            return redirectTo('../', request)
        
        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'pending'

        Page = pages.Ask('Ask', 'ask', filters)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.BLUE, session_response, config.color.ENDC)

        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Process(Resource):
    def render(self, request):
        response = {'error': True}

        try:
            action = request.args.get('action')[0]
        except:
            return redirectTo('../', request)

        response['error'] = False
        response['action'] = action
        
        if action == 'create':
            try:
                twitter_status_id = int(request.args.get('status_id')[0])
                print status_id
            except:
                twitter_status_id = 0

            response['ask'] = {
                    'twitter_status_id': str(twitter_status_id)
                } 

        if action == 'withdraw':
            try:
                ask_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../', request)

            response['ask'] = {
                    'id': ask_id 
                } 

        if action == 'engage':
            try:
                ask_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../', request)

            response['ask'] = {
                    'id': ask_id 
                } 

        return json.dumps(response)


class Create(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'save_order'
        
        #try:
        #    status_id = int(request.args.get('status_id')[0])
        #except:
        #    return redirectTo('../', request)

        twitter_status_id = request.args.get('twitter_status_id')[0]
        niche = request.args.get('niche')[0]
        campaign_type = request.args.get('campaign_type')[0]
        charge = int(request.args.get('price_per_retweet')[0])
        #campaign_type = request.args.get('campaign_type')[0]
        
        ## Handle quantity input
        #if not quantity:
        #    return json.dumps(dict(response=0, text=definitions.QUANTITY[0]))

        #try:
        #    quantity = int(quantity)
        #except:
        #    return json.dumps(dict(response=0, text=definitions.QUANTITY[1]))

        #if quantity < 0:
        #    return json.dumps(dict(response=0, text=definitions.QUANTITY[2]))

        ## Handle quantity input
        #if not amount:
        #    return json.dumps(dict(response=0, text=definitions.AMOUNT[0]))

        #try:
        #    amount = float(amount)
        #except:
        #    return json.dumps(dict(response=0, text=definitions.AMOUNT[1]))
        #
        ## Handle shipping_cost input
        #if not shipping_cost:
        #    return json.dumps(dict(response=0, text=definitions.SHIPPING_COST[0]))

        #try:
        #    shipping_cost = float(shipping_cost)
        #except:
        #    return json.dumps(dict(response=0, text=definitions.SHIPPING_COST[1]))


        timestamp = config.create_timestamp()

        data = {
            'status': 'active',
            'created_at': timestamp,
            'updated_at': timestamp,
            'twitter_name': session_user['twitter_name'],
            'twitter_status_id': twitter_status_id,
            'user_id': session_user['id'],
            'cost': charge,
            'campaign_type': campaign_type, 
            'niche': niche
        }

        new_ask = Ask(data)
        db.add(new_ask)

        client = db.query(Profile).filter(Profile.user_id == session_user['id']).first()
        client.available_balance -= charge
        client.reserved_balance += charge

        db.commit()

        #plain = mailer.offerMemoPlain(seller)
        #html = mailer.offerMemoHtml(seller)
        #Email(mailer.noreply, seller_email, 'You have a new offer at Coingig.com!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))


class Withdraw(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'withdraw_ask'

        is_confirmed = request.args.get('is_confirmed')[0]
        if is_confirmed == 'no':
            return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))
        
        try:
            ask_id = int(request.args.get('ask_id')[0])
        except:
            return redirectTo('../', request)
        
        ask = db.query(Ask).filter(Ask.id == ask_id).first()

        if ask.user_id != session_user['id']:
            return redirectTo('../', request)

        timestamp = config.create_timestamp()
        
        ask.updated_at = timestamp 
        ask.status = 'withdrawn'

        db.commit()
        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

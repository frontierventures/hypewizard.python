#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Bid, Order, Profile, User
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages
import twitter_api


def assemble(root):
    root.putChild('bid', Main())
    root.putChild('process_bid', Process())
    root.putChild('create_bid', Create())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_response = SessionManager(request).getSessionResponse()
        
        if session_user['id'] == 0:
            return redirectTo('../', request)
        
        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'pending'

        Page = pages.Bid('Bid', 'bid', filters)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.BLUE, session_response, config.color.ENDC)

        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Details(Element):
    def __init__(self, session_user, filters):
        self.session_user = session_user
        self.filters = filters

        template = 'templates/elements/bid_details.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.twitter_user = twitter_api.get_user(self.session_user['twitter_name'])

    @renderer
    def twitter_info(self, request, tag):
        slots = {}
        slots['name'] = str(self.twitter_user.name)
        slots['created_at'] = str(self.twitter_user.created_at)
        slots['statuses_count'] = str(self.twitter_user.statuses_count)
        slots['followers_count'] = str(self.twitter_user.followers_count)
        slots['market_score'] = str(0)
        #slots['status_text'] = status.text.encode('utf-8')
        yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []
        buttons.append({
            'url': '../process_bid?action=create&status_id=%s' % self.status.id,
            'caption': 'create' 
        })
        for button in buttons:
            slots = {}
            slots['caption'] = button['caption']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 


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

            response['bid'] = {
                    'twitter_status_id': str(twitter_status_id)
                } 

        print response

        if action == 'engage':
            try:
                bid_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../', request)

            #bid = db.query(Bid).filter(Bid.id == bid_id).first()
            response['bid'] = {
                    'id': bid_id, 
                } 
            
        return json.dumps(response)


class Create(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'create_bid'
        
        price_per_retweet = request.args.get('price_per_retweet')[0]
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
            'create_timestamp': timestamp,
            'update_timestamp': timestamp,
            'twitter_name': session_user['twitter_name'],
            'status_id': 0,
            'seller_id': session_user['id'] ,
            'buyer_id': 0,
            'cost': price_per_retweet,
            'campaign_type': ''
        }

        new_bid = Bid(data)
        db.add(new_bid)
        db.commit()

        #plain = mailer.offerMemoPlain(seller)
        #html = mailer.offerMemoHtml(seller)
        #Email(mailer.noreply, seller_email, 'You have a new offer at Coingig.com!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

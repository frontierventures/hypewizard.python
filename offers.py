#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Ask, Bid, Profile, Transaction, TwitterUserData, User
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
    root.putChild('offers', Main())
    root.putChild('process_offer', Process())
    root.putChild('complete_offer', Complete())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'offers'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'open'

        Page = pages.Offers('%s Offers' % config.company_name, 'offers', filters)
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

        offers = db.query(Transaction).filter(Transaction.promoter_id == session_user['id'])

        if filters['status'] == 'open':
            offers = offers.filter(Transaction.status.in_(['open', 'approved'])).order_by(Transaction.updated_at.desc())
        if filters['status'] == 'complete':
            offers = offers.filter(Transaction.status == 'complete').order_by(Transaction.updated_at.desc())

        if offers.count() == 0:
            template = 'templates/elements/empty_offers_table.xml'
        else:
            template = 'templates/elements/offers_table.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.offers = offers

    @renderer
    def count(self, request, tag):
        statuses = {
            'open': 'Open',
            'complete': 'Complete'
        }

        slots = {}
        slots['offer_status'] = statuses[self.filters['status']]
        slots['offer_count'] = str(self.offers.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def offer_status(self, request, tag):
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
        for index, offer in enumerate(self.offers):
            slots = {}
            slots['row_id'] = 'row_%s' % index
            slots['status'] = offer.status 
            slots['created_at'] = config.convert_timestamp(offer.created_at, config.STANDARD)
            slots['updated_at'] = config.convert_timestamp(offer.updated_at, config.STANDARD)
            slots['offer_id'] = str(offer.id)
            
            item = db.query(TwitterUserData).filter(TwitterUserData.twitter_id == offer.client_twitter_id).first()
            slots['client_twitter_name'] = item.twitter_name.encode('utf-8')

            slots['client_twitter_name_url'] = 'http://www.twitter.com/%s' % item.twitter_name
            slots['twitter_status_id'] = str(offer.twitter_status_id) 
            slots['twitter_status_id_url'] = 'http://www.twitter.com/%s/status/%s' % (item.twitter_name, offer.twitter_status_id)
            slots['charge'] = str(offer.charge) 
            self.offer = offer
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []
        
        if self.offer.status == 'approved':
            buttons.append({
                'url': '../process_offer?action=complete&id=%s' % self.offer.id,
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
        session_user['action'] = 'process_offer'

        response = {'error': True}
        try:
            action = request.args.get('action')[0]
        except:
            return redirectTo('../', request)

        if action == 'complete':
            try:
                offer_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../offers', request)

            response['error'] = False
            response['action'] = action

            response['offer'] = {
                    'id': str(offer_id)
                } 

            return json.dumps(response)


class Complete(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        
        time.sleep(2)
        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'complete_offer'

        is_confirmed = request.args.get('is_confirmed')[0]
        if is_confirmed == 'no':
            response = {}
            response['error'] = False
            response['message'] = definitions.MESSAGE_SUCCESS
            response['url'] = '../offers'
            return json.dumps(response) 
        
        try:
            offer_id = int(request.args.get('offer_id')[0])
        except:
            return redirectTo('../', request)
        
        offer = db.query(Transaction).filter(Transaction.id == offer_id).first()

        if offer.promoter_id != session_user['id']:
            return redirectTo('../', request)

        #####################################
        # Check Retweet Maturity
        #####################################
        
        response = twitter_api.get_retweet_duration(offer.promoter_twitter_id, offer.twitter_status_id)
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
                    response['message'] = 'Promotion period is 24 hrs. (Elapsed: %s)' % timestamp 
                    return json.dumps(response) 
            else:
                response = {}
                response['error'] = True
                response['message'] = 'Please retweet for your client'
                return json.dumps(response) 

        #####################################

        timestamp = config.create_timestamp()
        
        offer.updated_at = timestamp 
        offer.status = 'complete'

        client = db.query(Profile).filter(Profile.user_id == offer.client_id).first()
        client.offer_count -= 1
        client.reserved_balance -= offer.charge

        promoter = db.query(Profile).filter(Profile.user_id == offer.promoter_id).first()
        promoter.offer_count -= 1
        promoter.available_balance += offer.charge

        if offer.ask_id != 0:
            ask = db.query(Ask).filter(Ask.id == offer.ask_id).first()
            ask.target += 1

            if ask.target == ask.goal:
                ask.status = 'withdrawn'

        if offer.bid_id != 0:
            bid = db.query(Bid).filter(Bid.id == offer.bid_id).first()
            bid.tally += 1

        db.commit()

        plain = mailer.offer_complete_memo_plain(offer)
        html = mailer.offer_complete_memo_html(offer)
        Email(mailer.noreply, client.email, 'Your Hype Wizard transaction is complete!', plain, html).send()

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = '../offers?kind=complete'

        return json.dumps(response) 

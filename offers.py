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
    root.putChild('offers', Main())
    root.putChild('process_offer', Process())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'offers'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'open'

        Page = pages.Offers('Offers', 'offers', filters)
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

        offers = db.query(Transaction).filter(Transaction.client_id == session_user['id'])

        if filters['status'] == 'open':
            offers = offers.filter(Transaction.status.in_(['open', 'approved'])).order_by(Transaction.update_timestamp.desc())
        if filters['status'] == 'complete':
            offers = offers.filter(Transaction.status == 'complete').order_by(Transaction.update_timestamp.desc())

        if offers.count() == 0:
            template = 'templates/elements/no_offers_table.xml'
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
        for offer in self.offers:
            slots = {}
            slots['status'] = offer.status 
            slots['create_timestamp'] = config.convert_timestamp(offer.create_timestamp, config.STANDARD)
            slots['offer_id'] = str(offer.id)
            slots['promoter_twitter_name'] = offer.promoter_twitter_name.encode('utf-8')
            slots['promoter_twitter_name_url'] = 'http://www.twitter.com/%s' % offer.promoter_twitter_name
            slots['twitter_status_id'] = str(offer.twitter_status_id) 
            slots['twitter_status_id_url'] = 'http://www.twitter.com/%s/status/%s' % (offer.promoter_twitter_name, offer.twitter_status_id)
            slots['charge'] = str(offer.charge) 
            self.offer = offer
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []

        if self.offer.status == 'open':
            buttons.append({
                'url': '../process_offer?action=approve&id=%s' % self.offer.id,
                'caption': 'Approve' 
            })
            buttons.append({
                'url': '../process_offer?action=disapprove&id=%s' % self.offer.id,
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

        try:
            action = request.args.get('action')[0]
        except:
            return redirectTo('../', request)

        if action == 'approve':
            try:
                offer_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../offers', request)

            offer = db.query(Transaction).filter(Transaction.id == offer_id).first()
            if offer.client_id != session_user['id']:
                return redirectTo('../', request)

            offer.status = 'approved'
            db.commit()

            return redirectTo('../offers', request)

        if action in ['disapprove', 'withdraw']:
            try:
                offer_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../offers', request)

            offer = db.query(Transaction).filter(Transaction.id == offer_id).first()
            if offer.client_id != session_user['id']:
                return redirectTo('../', request)

            offer.status = 'cancelled'

            client = db.query(Profile).filter(Profile.user_id == offer.client_id).first()
            client.offer_count -= 1
            client.available_balance += offer.charge
            client.reserved_balance -= offer.charge

            promoter = db.query(Profile).filter(Profile.user_id == offer.promoter_id).first()
            promoter.transaction_count -= 1
            
            db.commit()

            return redirectTo('../offers', request)

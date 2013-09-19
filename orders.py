#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Ask, Order, Profile, User
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages


def assemble(root):
    root.putChild('orders', Main())
    root.putChild('process_order', Process())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_response = SessionManager(request).getSessionResponse()
        
        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'pending'

        Page = pages.Orders('Orders', 'orders', filters)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssession_response: %s%s" % (config.color.BLUE, session_response, config.color.ENDC)

        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Orders(Element):
    def __init__(self, session_user, filters):
        self.session_user = session_user
        self.filters = filters

        orders = db.query(Ask)
        if filters['status'] == 'pending':
            orders = orders.filter(Ask.status.in_(['open', 'paid'])).order_by(Ask.update_timestamp.desc())
        if filters['status'] == 'canceled':
            orders = orders.filter(Ask.status == 'canceled').order_by(Ask.update_timestamp.desc())
        if filters['status'] == 'complete':
            orders = orders.filter(Ask.status == 'received').order_by(Ask.update_timestamp.desc())

        if orders.count() == 0:
            template = 'templates/elements/no_orders.xml'
        else:
            template = 'templates/elements/orders.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.orders = orders

    @renderer
    def count(self, request, tag):
        statuses = {
            'pending': 'Pending',
            'canceled': 'Canceled',
            'complete': 'Complete'
        }

        slots = {}
        slots['order_status'] = statuses[self.filters['status']]
        slots['order_count'] = str(self.orders.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def order_status(self, request, tag):
        statuses = {
            'pending': 'Pending',
            'canceled': 'Canceled',
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
        for order in self.orders:
            timestamp = float(order.create_timestamp)

            slots = {}
            slots['create_timestamp'] = config.convert_timestamp(order.create_timestamp, config.STANDARD)
            slots['order_id'] = str(order.id)
            slots['twitter_name'] = 'http://www.twitter.com/%s' % order.twitter_name
            slots['status_id'] = str(order.status_id) 
            slots['cost'] = str(order.cost) 
            slots['campaign_type'] = str('') 
            self.order = order
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []

        buttons.append({
            'url': '../',
            'class': 'ticon view hint hint--top hint--rounded', 
            'hint': 'View Order Details'})

        buttons.append({
            'url': '../',
            'class': 'ticon remove hint hint--top hint--rounded', 
            'hint': 'Fullfil Offer'})

        for button in buttons:
            slots = {}
            slots['hint'] = button['hint']
            slots['class'] = button['class']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 


class Create(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'save_order'

        cost = request.args.get('cost')[0]
        message = request.args.get('message')[0]
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
            'status': 'open',
            'create_timestamp': timestamp,
            'update_timestamp': timestamp,
            'twitter_name': session_user['twitter_name'],
            'message': message,
            'seller_id': 0,
            'buyer_id': session_user['id'],
            'cost': cost,
            'campaign_type': ''
        }

        new_ask = Ask(data)
        db.add(new_ask)
        db.commit()

        #plain = mailer.offerMemoPlain(seller)
        #html = mailer.offerMemoHtml(seller)
        #Email(mailer.noreply, seller_email, 'You have a new offer at Coingig.com!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))


class Process(Resource):
    def render(self, request):
        response = {'error': True}
        try:
            action = request.args.get('action')[0]
        except:
            return redirectTo('../', request)

        response['error'] = False
        response['action'] = action

        if action != 'create':
            try:
                order_id = int(request.args.get('id')[0])
            except:
                return redirectTo('../', request)
       
            order = db.query(Order).filter(Order.id == order_id).first()

            response['order'] = {
                    'id': order.id 
                } 
        return json.dumps(response)

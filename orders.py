#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, Order
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages


def assemble(root):
    root.putChild('orders', Main())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'orders'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        session_response = SessionManager(request).get_session_response()

        filters = {}
        try:
            filters['status'] = request.args.get('status')[0]
        except:
            filters['status'] = 'open'

        Page = pages.Orders('%s Orders' % config.company_name, 'orders', filters)
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

        orders = db.query(Order).filter(Order.user_id == session_user['id'])

        if filters['status'] == 'open':
            orders = orders.filter(Order.status.in_(['open', 'approved'])).order_by(Order.updated_at.desc())
        if filters['status'] == 'complete':
            orders = orders.filter(Order.status == 'complete').order_by(Order.updated_at.desc())

        if orders.count() == 0:
            template = 'templates/elements/empty_orders_table.xml'
        else:
            template = 'templates/elements/orders_table.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.orders = orders

    @renderer
    def count(self, request, tag):
        statuses = {
            'open': 'Open',
            'complete': 'Complete'
        }

        slots = {}
        slots['order_status'] = statuses[self.filters['status']]
        slots['order_count'] = str(self.orders.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def order_status(self, request, tag):
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
        for order in self.orders:
            slots = {}
            slots['status'] = order.status 
            slots['created_at'] = config.convert_timestamp(order.created_at, config.STANDARD)
            slots['updated_at'] = config.convert_timestamp(order.updated_at, config.STANDARD)
            slots['order_id'] = str(order.id)
            slots['user_id'] = str(order.user_id)
            slots['btc_amount'] = str(order.btc_amount)
            slots['fiat_amount'] = str(order.fiat_amount)
            slots['currency'] = str(order.currency)
            self.order = order
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        buttons = []

        if self.order.status == 'open':
            buttons.append({
                'url': 'https://coinbase.com/checkouts/%s?c=a' % self.order.code,
                'caption': 'Invoice' 
            })

        for button in buttons:
            slots = {}
            slots = {}
            slots['caption'] = button['caption']
            slots['url'] = button['url']
            yield tag.clone().fillSlots(**slots) 

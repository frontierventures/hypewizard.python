#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Order
from data import db
from sessions import SessionManager


import coinbase
import config
import decimal
import definitions
import error
import json
import forms
import pages

D = decimal.Decimal
from coinbase import api
coinbase_api = api 


def assemble(root):
    root.putChild('deposit', Deposit())
    return root


class Deposit(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'deposit'

        deposit_amount = request.args.get('deposit_amount')[0]

        response = error.deposit_amount(request, deposit_amount)
        if response['error']:
            return json.dumps(response) 

        timestamp = config.create_timestamp()
            
        rates = coinbase_api.get_rates()

        fiat_amount = D(deposit_amount) * D(rates['buy'])

        data = {
            'status': 'open',
            'created_at': timestamp,
            'updated_at': timestamp,
            'user_id': session_user['id'],
            'currency': 'USD',
            'fiat_amount': float(fiat_amount),
            'btc_amount': deposit_amount,
            'code': '' 
        }

        new_order = Order(data)
        db.add(new_order)
        db.commit()

        data = {
            "name": "Hype Wizard Credit - %s BTC" % deposit_amount,
            "price_string": "%s" % deposit_amount,
            "price_currency_iso": "USD",
            "custom": "%s" % new_order.id,
            "callback_url": "http://www.example.com/my_custom_button_callback",
            "description": "Spendable Hype Wizard credit",
            "type": "buy_now",
            "style": "custom_large"
        }

        code = coinbase_api.create_invoice(data)

        order = db.query(Order).filter(Order.id == new_order.id).first()
        order.code = str(code)
        db.commit()

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = 'https://coinbase.com/checkouts/%s?c=a' % order.code

        return json.dumps(response) 

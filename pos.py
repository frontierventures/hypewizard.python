#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Order
from data import db
from sessions import SessionManager

from coinbase import api

#import coinbase
import config
import decimal
import definitions
import json
import forms
import pages

D = decimal.Decimal


def assemble(root):
    root.putChild('deposit', Deposit())
    return root


class Deposit(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'deposit'

        deposit_amount = request.args.get('deposit_amount')[0]

        timestamp = config.create_timestamp()
            
        rates = api.get_rates()

        fiat_amount = D(deposit_amount) * D(rates['buy'])

        data = {
            'status': 'open',
            'created_at': timestamp,
            'updated_at': timestamp,
            'user_id': session_user['id'],
            'currency': 'USD',
            'fiat_amount': float(fiat_amount),
            'btc_amount': deposit_amount,
        }

        new_order = Order(data)
        db.add(new_order)
        db.commit()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

from coinbase import CoinbaseAccount

if __name__ == '__main__':
    api.get_rates_test()

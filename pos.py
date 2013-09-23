#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Order
from data import db
from sessions import SessionManager

import config
import definitions
import json
import forms
import pages


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

        data = {
            'status': 'open',
            'created_at': timestamp,
            'updated_at': timestamp,
            'user_id': session_user['id'],
            'currency': 'USD',
            'fiat_amount': 0,
            'btc_amount': 0,
        }

        new_order = Order(data)
        db.add(new_order)
        db.commit()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))

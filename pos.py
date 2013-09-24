#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Order, Profile
from data import db
from sessions import SessionManager


import coinbase
import config
import decimal
import definitions
import error
import functions
import hashlib
import json
import forms
import pages

D = decimal.Decimal
from coinbase import api
coinbase_api = api 


def assemble(root):
    root.putChild('callback', Callback())
    root.putChild('deposit', Deposit())
    root.putChild('withdraw', Withdraw())
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

        satoshi_deposit_amount = D(deposit_amount) * D(100000000)
        satoshi_deposit_amount = int(satoshi_deposit_amount)

        data = {
            'status': 'open',
            'created_at': timestamp,
            'updated_at': timestamp,
            'kind': 'deposit',
            'user_id': session_user['id'],
            'currency': 'USD',
            'fiat_amount': float(fiat_amount),
            'btc_amount': satoshi_deposit_amount, 
            'code': '', 
            'token': '' 
        }

        new_order = Order(data)
        db.add(new_order)
        db.commit()

        token = hashlib.sha224(str(data)).hexdigest()

        data = {
            "name": "Hype Wizard Credit - %s BTC" % deposit_amount,
            "price_string": "%s" % deposit_amount,
            "price_currency_iso": "BTC",
            "custom": "%s" % new_order.id,
            "callback_url": "%s/callback?token=%s" % (config.company_url, token),
            "description": "Spendable Hype Wizard credit",
            "type": "buy_now",
            "style": "custom_large"
        }

        code = coinbase_api.create_invoice(data)

        order = db.query(Order).filter(Order.id == new_order.id).first()
        order.code = str(code)
        order.token = str(token)
        db.commit()

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = 'https://coinbase.com/checkouts/%s?c=a' % order.code
        return json.dumps(response) 


class Withdraw(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'withdraw'
        
        amount = request.args.get('amount')[0]
        bitcoin_address = request.args.get('bitcoin_address')[0]
        
        response = error.withdraw_amount(request, amount)
        if response['error']:
            return json.dumps(response) 
        
        response = error.bitcoin_address(request, bitcoin_address)
        if response['error']:
            return json.dumps(response) 

        profile = db.query(Profile).filter(Profile.id == session_user['id']).first()

        if D(profile.available_balance) < D(amount):
            response = {}
            response['error'] = True
            response['message'] = "You can withdraw %s max." % profile.available_balance 
            response['url'] = '../account'
            return json.dumps(response) 

        timestamp = config.create_timestamp()

        rates = coinbase_api.get_rates()
        fiat_amount = D(amount) * D(rates['sell'])

        data = {
            'status': 'open',
            'created_at': timestamp,
            'updated_at': timestamp,
            'kind': 'withdraw',
            'user_id': session_user['id'],
            'currency': 'USD',
            'fiat_amount': float(fiat_amount),
            'btc_amount': amount,
            'code': '' 
        }

        new_order = Order(data)
        db.add(new_order)

        profile.available_balance = D(profile.available_balance) - D(amount) 
        db.commit()

        functions.refresh_session_user(request)

        response = {}
        response['error'] = False
        response['message'] = definitions.MESSAGE_SUCCESS
        response['url'] = '../orders'
        return json.dumps(response) 
 

class Callback(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        try:
            token = request.args.get('token')[0]
        except:
            token = ''

        if token:
            orders = db.query(Order).filter(Order.status == 'open')
            order = orders.filter(Order.token == token).first()

        if order:
            profile = db.query(Profile).filter(Profile.user_id == order.user_id).first()

            new_balance_satoshi = D(profile.available_balance) + D(order.btc_amount)
            profile.available_balance += int(new_balance_satoshi) 

            order.status = 'complete'
            # credit balance
            db.commit()

        print 'Callback from Coinbase\n' * 20
        request.setResponseCode(200)
        return 'OK' 

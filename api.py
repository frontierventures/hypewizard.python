from twisted.web.resource import Resource
from twisted.web.util import redirectTo

import config
import definitions
import functions
import json
import twitter_api

from data import Ask, Bid, Profile 
from data import db
from sqlalchemy.sql import and_
from sqlalchemy.sql import func

from sessions import SessionManager
import definitions


def assemble(root):
    root.putChild('get_asks', GetAsks())
    root.putChild('get_bids', GetBids())
    root.putChild('get_user', GetMarketScore())
    return root


class GetAsks(Resource):
    def render(self, request):
        response = {'error': True}

        session_user = SessionManager(request).get_session_user()

        response['rule'] = 'none'
        if session_user['id'] == 0:
            response['rule'] = 'limit'

        asks = db.query(Ask).filter(Ask.status == 'active')
        asks = asks.order_by(Ask.create_timestamp.desc())

        orders = []
        for ask in asks: 
            order = {}
            order['id'] = ask.id
            order['twitter_name'] = ask.twitter_name
            order['status_id'] = ask.status_id
            order['cost'] = ask.cost
            orders.append(order)

        response['orders'] = orders
        response['error'] = False

        return json.dumps(response)


class GetBids(Resource):
    def render(self, request):
        response = {'error': True}

        session_user = SessionManager(request).get_session_user()

        response['rule'] = 'none'
        if session_user['id'] == 0:
            response['rule'] = 'limit'

        bids = db.query(Bid).filter(Bid.status == 'active')
        bids = bids.order_by(Bid.create_timestamp.desc())

        orders = []
        for bid in bids: 
            order = {}
            order['id'] = bid.id
            order['twitter_name'] = bid.twitter_name
            order['status_id'] = bid.status_id
            order['cost'] = bid.cost
            orders.append(order)

        response['orders'] = orders
        response['error'] = False

        return json.dumps(response)


class GetMarketScore(Resource):
    def render(self, request):
        session_user = SessionManager(request).get_session_user()

        try:
            twitter_name = request.args.get('twitter_name')[0]
        except:
            return redirectTo('../', request)

        user = twitter_api.get_user(twitter_name)

        profiles = db.query(Profile).filter(Profile.twitter_name == twitter_name)
        profile = profiles.order_by(Profile.create_timestamp.desc()).first()

        record = {}
        record['score'] = 100
        record['statuses_count'] = user.statuses_count 
        record['followers_count'] = user.followers_count
        record['niche'] = definitions.niches[profile.niche]
        return json.dumps(record)

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
        asks = asks.order_by(Ask.created_at.desc())

        orders = []
        for ask in asks: 
            order = {}
            order['id'] = ask.id
            order['niche'] = definitions.niches[ask.niche]
            order['campaign_type'] = definitions.campaign_types[ask.campaign_type]
            order['twitter_name'] = ask.twitter_name
            order['twitter_status_id'] = ask.twitter_status_id
            order['cost'] = ask.cost

            order['rule'] = 'none'
            if ask.user_id != session_user['id']:
                order['rule'] = 'limit'

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
        bids = bids.order_by(Bid.created_at.desc())

        orders = []
        for bid in bids: 
            order = {}
            order['id'] = bid.id
            order['niche'] = definitions.niches[bid.niche]
            order['campaign_type'] = definitions.campaign_types[bid.campaign_type]
            order['twitter_name'] = bid.twitter_name
            order['twitter_status_id'] = bid.twitter_status_id
            order['cost'] = bid.cost

            order['rule'] = 'none'
            if bid.user_id != session_user['id']:
                order['rule'] = 'limit'

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
        profile = profiles.order_by(Profile.created_at.desc()).first()

        record = {}
        record['score'] = 100
        record['statuses_count'] = user.statuses_count 
        record['followers_count'] = user.followers_count
        record['niche'] = definitions.niches[profile.niche]
        return json.dumps(record)

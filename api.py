from twisted.web.resource import Resource
from twisted.web.util import redirectTo

import config
import definitions
import functions
import json
import twitter_api

from data import Ask, Bid, Profile, Transaction, TwitterUserData, Tweet 
from data import db
from sqlalchemy.sql import and_
from sqlalchemy.sql import func

from sessions import SessionManager
import definitions


def assemble(root):
    root.putChild('get_asks', GetAsks())
    root.putChild('get_bids', GetBids())
    root.putChild('get_session_user', GetSessionUser())
    root.putChild('get_user', GetMarketScore())
    root.putChild('get_transactions', GetTransactions())
    return root


class GetAsks(Resource):
    def render(self, request):
        response = {'error': True}

        session_user = SessionManager(request).get_session_user()

        asks = db.query(Ask).filter(Ask.status == 'active')
        asks = asks.order_by(Ask.created_at.desc())

        orders = []
        for ask in asks: 
            order = {}
            order['id'] = ask.id
            order['niche'] = definitions.niches[ask.niche]
            order['campaign_type'] = definitions.campaign_types[ask.campaign_type]

            item = db.query(TwitterUserData).filter(TwitterUserData.twitter_id == ask.twitter_id).first()
            order['twitter_name'] = item.twitter_name 
            
            tweet = db.query(Tweet).filter(Tweet.twitter_status_id == ask.twitter_status_id).first()

            if not tweet:
                twitter_status = twitter_api.get_status(ask.twitter_status_id) 
                data = {
                    'twitter_status_id': ask.twitter_status_id,
                    'created_at': twitter_status.created_at.encode('utf-8'),
                    'text': twitter_status.text.encode('utf-8')
                }
                new_tweet = Tweet(data)
                db.add(new_tweet)

                order['twitter_status_text'] = twitter_status.text.encode('utf-8')
            else:
                order['twitter_status_text'] = tweet.text

            order['twitter_status_id'] = ask.twitter_status_id

            order['cost'] = ask.cost
            order['target'] = ask.target
            order['goal'] = ask.goal
           
            order['engage'] = {
                'is_allowed': True
            }

            if ask.user_id == session_user['id']:
                order['engage']['is_allowed'] = False
                order['engage']['reason'] = 'different_user'

            if not session_user['is_email_verified']:
                order['engage']['is_allowed'] = False
                order['engage']['reason'] = 'unverified'

            if session_user['id'] == 0:
                order['engage']['is_allowed'] = False
                order['engage']['reason'] = 'unauthorized'

            else:
                #transactions = db.query(Transaction).filter(Transaction.status == 'open')
                transactions = db.query(Transaction).filter(Transaction.ask_id == ask.id)
                transactions = transactions.filter(Transaction.promoter_id == session_user['id'])
                transaction = transactions.filter(Transaction.status == 'open').first()

                if transaction:
                    order['engage']['is_allowed'] = False
                    order['engage']['reason'] = 'engaged'

                transaction = transactions.filter(Transaction.status == 'approved').first()
                if transaction:
                    order['engage']['is_allowed'] = False
                    order['engage']['reason'] = 'approved'

            orders.append(order)

        response['orders'] = orders
        response['error'] = False

        return json.dumps(response)


class GetBids(Resource):
    def render(self, request):
        response = {'error': True}

        session_user = SessionManager(request).get_session_user()

        #response['rule'] = 'none'

        #if session_user['id'] == 0:
        #    response['rule'] = 'limit'

        bids = db.query(Bid).filter(Bid.status == 'active')
        bids = bids.order_by(Bid.created_at.desc())

        orders = []
        for bid in bids: 
            order = {}
            order['id'] = bid.id
            order['niche'] = definitions.niches[bid.niche]
            order['campaign_type'] = definitions.campaign_types[bid.campaign_type]

            order['twitter_id'] = bid.twitter_id 

            item = db.query(TwitterUserData).filter(TwitterUserData.twitter_id == bid.twitter_id).first()
            order['twitter_name'] = item.twitter_name 

            order['twitter_status_id'] = bid.twitter_status_id
            order['cost'] = bid.cost

            order['rule'] = 'none'
            if bid.user_id != session_user['id']:
                order['rule'] = 'limit'

            orders.append(order)
           
            order['engage'] = {
                'is_allowed': True
            }

            if bid.user_id == session_user['id']:
                order['engage']['is_allowed'] = False
                order['engage']['reason'] = 'different_user'

            if not session_user['is_email_verified']:
                order['engage']['is_allowed'] = False
                order['engage']['reason'] = 'unverified'

            if session_user['id'] == 0:
                order['engage']['is_allowed'] = False
                order['engage']['reason'] = 'unauthorized'

            else:
                transactions = db.query(Transaction).filter(Transaction.status == 'approved')
                transactions = transactions.filter(Transaction.client_id == session_user['id'])
                transaction = transactions.filter(Transaction.promoter_id == bid.user_id).first()
                #transaction = transactions.filter(Transaction.twitter_status_id == ask.twitter_status_id).first()

                print transaction

                if transaction:
                    order['engage']['is_allowed'] = False
                    order['engage']['reason'] = 'engaged'

        response['orders'] = orders
        response['error'] = False

        return json.dumps(response)


class GetTransactions(Resource):
    def render(self, request):
        response = {'error': True}

        session_user = SessionManager(request).get_session_user()
        session_user['action'] = 'get_transactions'

        if session_user['id'] == 0:
            return redirectTo('../', request)
    
        transactions = db.query(Transaction).filter(Transaction.client_id == session_user['id'])
        transactions = db.query(Transaction).filter(Transaction.status.in_(['open', 'approved']))
        transactions = transactions.order_by(Transaction.created_at.desc())

        records = []
        for transaction in transactions: 
            record = {}
            record['status'] = transaction.status
            record['kind'] = transaction.kind
            record['created_at'] = transaction.created_at
            record['updated_at'] = transaction.updated_at
            record['id'] = transaction.id
            # Pull Twitter user data
            twitter_user_data = db.query(TwitterUserData).filter(TwitterUserData.twitter_id == transaction.promoter_twitter_id).first()

            record['promoter_twitter_name'] = twitter_user_data.twitter_name 
            record['promoter_twitter_image'] = twitter_user_data.twitter_image 
            record['ask_id'] = transaction.ask_id

            record['wizard_score'] = "MY WIZARD SCORE" 

            record['twitter_status_id'] = transaction.twitter_status_id
            record['charge'] = transaction.charge
            records.append(record)

        response['transactions'] = records
        response['error'] = False

        return json.dumps(response)


class GetMarketScore(Resource):
    def render(self, request):
        session_user = SessionManager(request).get_session_user()

        try:
            twitter_id = request.args.get('twitter_id')[0]
        except:
            return redirectTo('../', request)

        #user = twitter_api.get_user(twitter_name)
        twitter_user = twitter_api.get_user_by_id(twitter_id)

        profiles = db.query(Profile).filter(Profile.twitter_id == twitter_user.id)
        profile = profiles.order_by(Profile.created_at.desc()).first()

        record = {}
        record['score'] = 100
        record['statuses_count'] = twitter_user.statuses_count 
        record['followers_count'] = twitter_user.followers_count
        record['niche'] = definitions.niches[profile.niche]
        return json.dumps(record)
        session_response = SessionManager(request).get_session_response()

        reponse = {}
        return json.dumps(record)


class GetSessionUser(Resource):
    def render(self, request):
        session_user = SessionManager(request).get_session_user()
        return json.dumps(session_user)

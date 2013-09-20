#
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from re import sub

import config
import definitions
import encryptor

engine = create_engine(config.db_connection_string)
Session = sessionmaker(bind=engine)
db = Session()

Base = declarative_base()

#used when threads are created
def reconnect():
    global engine
    global Session
    global db
    engine = create_engine(config.db_connection_string)
    Session = sessionmaker(bind=engine)
    db = Session()


class Ask(Base):
    __tablename__ = 'asks'
    id = Column(Integer, Sequence('ask_id_seq'), primary_key=True)
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    twitter_name = Column(String)
    twitter_status_id = Column(String)
    user_id = Column(Integer)
    target = Column(Integer)
    cost = Column(Integer)
    campaign_type = Column(String)
    niche = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.twitter_name = data['twitter_name']
        self.twitter_status_id = data['twitter_status_id'] 
        self.user_id = data['user_id']
        self.target = data['target']
        self.cost = data['cost']
        self.campaign_type = data['campaign_type']
        self.niche = data['niche']


class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, Sequence('bid_id_seq'), primary_key=True)
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    twitter_name = Column(String)
    twitter_status_id = Column(String)
    user_id = Column(Integer)
    cost = Column(Integer)
    campaign_type = Column(String)
    niche = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.twitter_name = data['twitter_name']
        self.twitter_status_id = data['twitter_status_id'] 
        self.user_id = data['user_id']
        self.cost = data['cost']
        self.campaign_type = data['campaign_type']
        self.niche = data['niche']

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    user_id = Column(Integer)
    action = Column(String)
    note = Column(String)

    def __init__(self, data):
        self.timestamp = data['timestamp']
        self.user_id = data['user_id']
        self.action = data['action']
        self.note = data['note']


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, Sequence('offer_id_seq'), primary_key=True)
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    client_twitter_name = Column(String)
    promoter_twitter_name = Column(String)
    twitter_status_id = Column(String)
    client_id = Column(Integer)
    promoter_id = Column(Integer)
    charge = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.client_twitter_name = data['client_twitter_name']
        self.promoter_twitter_name = data['promoter_twitter_name']
        self.twitter_status_id = data['twitter_status_id'] 
        self.client_id = data['client_id']
        self.promoter_id = data['promoter_id']
        self.charge = data['charge']


#class Order(Base):
#    __tablename__ = 'orders'
#    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
#    status = Column(String)
#    created_at = Column(String)
#    updated_at = Column(String)
#    twitter_name = Column(String)
#    seller_id = Column(Integer)
#    buyer_id = Column(Integer)
#    cost = Column(String)
#    campaign_type = Column(String)
#
#    def __init__(self, data):
#        self.status = data['status']
#        self.created_at = data['created_at']
#        self.updated_at = data['updated_at']
#        self.twitter_name = data['twitter_name']
#        self.seller_id = data['seller_id']
#        self.buyer_id = data['buyer_id']
#        self.cost = data['cost']
#        self.campaign_type = data['campaign_type']


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, Sequence('profile_id_seq'), primary_key=True)
    created_at = Column(String)
    updated_at = Column(String)
    token = Column(String)
    available_balance = Column(Integer)
    reserved_balance = Column(Integer)
    bitcoin_address = Column(String)
    twitter_name = Column(String)
    niche = Column(String)
    offer_count = Column(Integer)
    transaction_count = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('profiles', order_by=id))

    def __init__(self, data):
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.token = data['token']
        self.available_balance = data['available_balance']
        self.reserved_balance = data['reserved_balance']
        self.bitcoin_address = data['bitcoin_address']
        self.twitter_name = data['twitter_name']
        self.niche = data['niche']
        self.offer_count = data['offer_count']
        self.transaction_count = data['transaction_count']


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    client_twitter_name = Column(String)
    promoter_twitter_name = Column(String)
    twitter_status_id = Column(String)
    client_id = Column(Integer)
    promoter_id = Column(Integer)
    charge = Column(Integer)
    ask_id = Column(Integer)

    def __init__(self, data):
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.client_twitter_name = data['client_twitter_name']
        self.promoter_twitter_name = data['promoter_twitter_name']
        self.twitter_status_id = data['twitter_status_id'] 
        self.client_id = data['client_id']
        self.promoter_id = data['promoter_id']
        self.charge = data['charge']
        self.ask_id = data['ask_id']


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    status = Column(String)
    level = Column(Integer)
    login_timestamp = Column(String)
    email = Column(String)
    password = Column(String)
    is_email_verified = Column(Boolean)
    ip = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.level = data['level']
        self.login_timestamp = data['login_timestamp']
        self.email = data['email']
        self.password = data['password']
        self.is_email_verified = data['is_email_verified']
        self.ip = data['ip']


def reset(default):
    Base.metadata.create_all(engine)
    
    if default:
        timestamp = config.create_timestamp()

        user = db.query(User).filter(User.email == '0@0.0').first()
        if not user:
            data = {
                'status': 'available',
                'level': 0,
                'login_timestamp': timestamp,
                'email': '0@0.0',
                'password': encryptor.hash_password('0'),
                'is_email_verified': False,
                'ip': 0
            }
            user = User(data)

            data = {
                'created_at': timestamp,
                'updated_at': timestamp,
                'token': '',
                'bitcoin_address': '',
                'available_balance': 0,
                'reserved_balance': 0,
                'twitter_name': '',
                'niche': 'AA',
                'transaction_count': 0, 
                'offer_count': 0 
            }
            profile = Profile(data)
            user.profiles = [profile]

            db.add(user)

        user = db.query(User).filter(User.email == 'a@a.a').first()
        if not user:
            data = {
                'status': 'available',
                'level': 1,
                'login_timestamp': timestamp,
                'email': 'a@a.a',
                'password': encryptor.hash_password('a'),
                'is_email_verified': False,
                'ip': 0
            }
            user = User(data)

            data = {
                'created_at': timestamp,
                'updated_at': timestamp,
                'token': '',
                'bitcoin_address': '',
                'available_balance': 10000,
                'reserved_balance': 0,
                'twitter_name': 'coingig',
                'niche': 'AA',
                'transaction_count': 0,
                'offer_count': 0
            }
            profile = Profile(data)
            user.profiles = [profile]

            db.add(user)

        user = db.query(User).filter(User.email == 'b@b.b').first()
        if not user:
            data = {
                'status': 'available',
                'level': 1,
                'login_timestamp': timestamp,
                'email': 'b@b.b',
                'password': encryptor.hash_password('b'),
                'is_email_verified': False,
                'ip': 0
            }
            user = User(data)

            data = {
                'created_at': timestamp,
                'updated_at': timestamp,
                'token': '',
                'bitcoin_address': '',
                'available_balance': 10000,
                'reserved_balance': 0,
                'twitter_name': 'hypewizard',
                'niche': 'AA',
                'transaction_count': 0, 
                'offer_count': 0 
            }
            profile = Profile(data)
            user.profiles = [profile]

            db.add(user)

        db.commit()
        print "User account added"

    print "Database reset complete"

#flood(863)

reset(True)

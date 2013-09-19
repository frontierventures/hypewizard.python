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
    create_timestamp = Column(String)
    update_timestamp = Column(String)
    twitter_name = Column(String)
    status_id = Column(String)
    seller_id = Column(Integer)
    buyer_id = Column(Integer)
    cost = Column(String)
    campaign_type = Column(String)
    niche = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.create_timestamp = data['create_timestamp']
        self.update_timestamp = data['update_timestamp']
        self.twitter_name = data['twitter_name']
        self.status_id = data['status_id'] 
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
        self.cost = data['cost']
        self.campaign_type = data['campaign_type']
        self.niche = data['niche']


class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, Sequence('bid_id_seq'), primary_key=True)
    status = Column(String)
    create_timestamp = Column(String)
    update_timestamp = Column(String)
    twitter_name = Column(String)
    status_id = Column(String)
    seller_id = Column(Integer)
    buyer_id = Column(Integer)
    cost = Column(String)
    campaign_type = Column(String)
    niche = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.create_timestamp = data['create_timestamp']
        self.update_timestamp = data['update_timestamp']
        self.twitter_name = data['twitter_name']
        self.status_id = data['status_id'] 
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
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


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    status = Column(String)
    create_timestamp = Column(String)
    update_timestamp = Column(String)
    twitter_name = Column(String)
    seller_id = Column(Integer)
    buyer_id = Column(Integer)
    cost = Column(String)
    campaign_type = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.create_timestamp = data['create_timestamp']
        self.update_timestamp = data['update_timestamp']
        self.twitter_name = data['twitter_name']
        self.seller_id = data['seller_id']
        self.buyer_id = data['buyer_id']
        self.cost = data['cost']
        self.campaign_type = data['campaign_type']


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, Sequence('profile_id_seq'), primary_key=True)
    create_timestamp = Column(String)
    update_timestamp = Column(String)
    token = Column(String)
    balance = Column(String)
    bitcoin_address = Column(String)
    twitter_name = Column(String)
    niche = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('profiles', order_by=id))

    def __init__(self, data):
        self.create_timestamp = data['create_timestamp']
        self.update_timestamp = data['update_timestamp']
        self.token = data['token']
        self.balance = data['balance']
        self.bitcoin_address = data['bitcoin_address']
        self.twitter_name = data['twitter_name']
        self.niche = data['niche']


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    status = Column(String)
    create_timestamp = Column(String)
    update_timestamp = Column(String)
    client_twitter_name = Column(String)
    promoter_twitter_name = Column(String)
    twitter_status_id = Column(String)
    client_id = Column(Integer)
    promoter_id = Column(Integer)
    charge = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.create_timestamp = data['create_timestamp']
        self.update_timestamp = data['update_timestamp']
        self.client_twitter_name = data['client_twitter_name']
        self.promoter_twitter_name = data['promoter_twitter_name']
        self.twitter_status_id = data['twitter_status_id'] 
        self.client_id = data['client_id']
        self.promoter_id = data['promoter_id']
        self.charge = data['charge']


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
                'create_timestamp': timestamp,
                'update_timestamp': timestamp,
                'token': '',
                'bitcoin_address': '',
                'balance': 0,
                'twitter_name': '',
                'niche': ''
            }
            profile = Profile(data)
            user.profiles = [profile]

            db.add(user)

        db.commit()
        print "User account added"

    print "Database reset complete"

#flood(863)

reset(True)

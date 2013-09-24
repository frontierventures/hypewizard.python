from twisted.web.resource import Resource
from sessions import SessionManager

from data import Profile, User
from data import db

from sessions import SessionManager

import config
import decimal
import definitions
import inspect
import json

from decimal import ROUND_UP
D = decimal.Decimal


def refresh_session_user(request):
    session_user = SessionManager(request).get_session_user()
    profile = db.query(Profile).filter(Profile.user_id == session_user['id']).first()
    
    session_user['available_balance'] = profile.available_balance
    session_user['reserved_balance'] = profile.reserved_balance

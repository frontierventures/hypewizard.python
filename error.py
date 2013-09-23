#!/usr/bin/env python
import definitions
import re
from sessions import SessionManager


def old_password(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.PASSWORD[0]
    return response


def new_password(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.PASSWORD[0]
    return response


def new_password_repeat(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.PASSWORD[0]
    return response


def bitcoin_address(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.BITCOIN_ADDRESS[0]
    elif not re.match(definitions.REGEX_BITCOIN_ADDRESS, value):
        response['error'] = True
        response['message'] = definitions.BITCOIN_ADDRESS[1]
    return response


def password_match(request, value1, value2):
    response = {}
    response['error'] = False

    if value1 != value2:
        response['error'] = True
        response['message'] = definitions.PASSWORD_REPEAT[2]
    return response


def email(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.EMAIL[0]
    elif not re.match(definitions.REGEX_EMAIL, value):
        response['error'] = True
        response['message'] = definitions.EMAIL[1]
    return response


def twitter_name(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.TWITTER_NAME[0]
    return response


def deposit_amount(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.DEPOSIT_AMOUNT[0]

    try:
        value = float(value)
    except:
        response['error'] = True
        response['message'] = definitions.DEPOSIT_AMOUNT[1]

    if value <= 0:
        response['error'] = True
        response['message'] = definitions.DEPOSIT_AMOUNT[1]

    return response


def price_per_tweet(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.PRICE_PER_TWEET[0]

    try:
        value = float(value)
    except:
        response['error'] = True
        response['message'] = definitions.PRICE_PER_TWEET[1]

    if value <= 0:
        response['error'] = True
        response['message'] = definitions.PRICE_PER_TWEET[1]

    return response


def goal(request, value):
    response = {}
    response['error'] = False

    if not value:
        response['error'] = True
        response['message'] = definitions.RETWEET_GOAL[0]

    try:
        value = int(value)
    except:
        response['error'] = True
        response['message'] = definitions.RETWEET_GOAL[1]

    if value <= 0:
        response['error'] = True
        response['message'] = definitions.RETWEET_GOAL[1]

    return response

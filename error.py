#!/usr/bin/env python
import definitions
import re
from sessions import SessionManager


#def bitcoin_address(request, value):
#    response = {}
#    error = False
#    if not value:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.BITCOIN_ADDRESS[0]})
#        return True
#    elif not re.match(definitions.REGEX_BITCOIN_ADDRESS, value):
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.BITCOIN_ADDRESS[1]})
#        return True


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
    #if not value:
    #    SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[0]})
    #    return True
    #elif not re.match(definitions.REGEX_EMAIL, value):
    #    SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[1]})
    #    return True


#def new_password_repeat(request, value):
#    if not value:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD_REPEAT[0]})
#        return True
##    elif not re.match(definitions.REGEX_PASSWORD, value):
##        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD_REPEAT[1]})
##        return True
#
#
#def password_mismatch(request, value1, value2):
#    if value1 != value2:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD_REPEAT[2]})
#        return True
#
#
#def amount(request, value):
#    if not value:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.AMOUNT[0]})
#        return True
#    #elif not re.match(definitions.REGEX_FIRST, value):
#    #    SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.FIRST[1]})
#    #    return True
#
#
#def first(request, value):
#    if not value:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.FIRST[0]})
#        return True
#    elif not re.match(definitions.REGEX_FIRST, value):
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.FIRST[1]})
#        return True
#
#
#def last(request, value):
#    if not value:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.LAST[0]})
#        return True
#    elif not re.match(definitions.REGEX_LAST, value):
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.LAST[1]})
#        return True
#
#
#def email(request, value):
#    if not value:
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[0]})
#        return True
#    elif not re.match(definitions.REGEX_EMAIL, value):
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[1]})
#        return True

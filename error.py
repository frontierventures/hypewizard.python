#!/usr/bin/env python
import definitions
import re
from sessions import SessionManager


def amount(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.AMOUNT[0]})
        return True
    #elif not re.match(definitions.REGEX_FIRST, value):
    #    SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.FIRST[1]})
    #    return True


def first(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.FIRST[0]})
        return True
    elif not re.match(definitions.REGEX_FIRST, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.FIRST[1]})
        return True


def last(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.LAST[0]})
        return True
    elif not re.match(definitions.REGEX_LAST, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.LAST[1]})
        return True


def email(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[0]})
        return True
    elif not re.match(definitions.REGEX_EMAIL, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[1]})
        return True


def password(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD[0]})
        return True
#    elif not re.match(definitions.REGEX_PASSWORD, value):
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD[1]})
#        return True


def repeatPassword(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD_REPEAT[0]})
        return True
#    elif not re.match(definitions.REGEX_PASSWORD, value):
#        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD_REPEAT[1]})
#        return True


def mismatchPassword(request, value1, value2):
    if value1 != value2:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD_REPEAT[2]})
        return True


def bitcoinAddress(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.BITCOIN_ADDRESS[0]})
        return True
    elif not re.match(definitions.REGEX_BITCOIN_ADDRESS, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.BITCOIN_ADDRESS[1]})
        return True


def signature(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.SIGNATURE[0]})
        return True
    elif not re.match(definitions.REGEX_BITCOIN_ADDRESS, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.SIGNATURE[1]})
        return True


def productName(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TITLE[0]})
        return True
    elif not re.match(definitions.REGEX_TITLE, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TITLE[1]})
        return True


def productDescription(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.DESCRIPTION[0]})
        return True
    elif not re.match(definitions.REGEX_DESCRIPTION, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.DESCRIPTION[1]})
        return True

    if len(value) > 2000 or len(value) < 5:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.DESCRIPTION[2]})
        return True


def sellerNote(request, value):
    if not re.match(definitions.REGEX_NOTE, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.NOTE[1]})
        return True


def phone(request, value):
    if not re.match(definitions.REGEX_PHONE, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PHONE[1]})
        return True


def address1(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.ADDRESS1[0]})
        return True
    elif not re.match(definitions.REGEX_STREET_ADDRESS_1, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.ADDRESS1[1]})
        return True


def address2(request, value):
    if not re.match(definitions.REGEX_STREET_ADDRESS_2, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.ADDRESS2[1]})
        return True


def city(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.CITY[0]})
        return True
    elif not re.match(definitions.REGEX_CITY, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.CITY[1]})
        return True


def state(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.STATE[0]})
        return True
    elif not re.match(definitions.REGEX_STATE, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.STATE[1]})
        return True


def zip(request, value):
    if not value:
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.ZIP[0]})
        return True
    elif not re.match(definitions.REGEX_ZIP, value):
        SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.ZIP[1]})
        return True

#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from sessions import SessionManager

import twitter_api
import config
import locale
import pages

from data import db
from sqlalchemy.sql import and_
from data import Profile
from sessions import SessionManager


def assemble(root):
    root.putChild('account', Main())
    return root


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        session_user['page'] = 'account'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        Page = pages.Account('Account', 'account')
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Details(Element):
    def __init__(self, session_user):
        self.session_user = session_user

        self.profile = db.query(Profile).filter(Profile.id == session_user['id']).first()

        if session_user['status'] == 'verified':
            template = 'templates/elements/verified_account.xml'
        else:
            template = 'templates/elements/unverified_account.xml'

        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['slot_twitter_name'] = self.profile.twitter_name
        slots['slot_twitter_followers_count'] = str(twitter_api.get_followers_count(self.profile.twitter_name))
        yield tag.clone().fillSlots(**slots)


#class Details(Element):
#    def __init__(self, session_user):
#        self.session_user = session_user
#
#        self.lender = db.query(Profile).filter(Profile.id == session_user['id']).first()
#        self.solicitor = db.query(Profile).filter(Profile.id == 1).first()
#
#        if session_user['status'] == 'verified':
#            template = 'templates/elements/account0.xml'
#        else:
#            template = 'templates/elements/account1.xml'
#
#        self.loader = XMLString(FilePath(template).getContent())
#
#    @renderer
#    def details(self, request, tag):
#        locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
#
#        price = db.query(Price).filter(Price.currencyId == 'USD').first()
#
#        lenderBalanceBTC = float(self.lender.balance) / float(price.last)
#        solicitorBalanceBTC = float(self.solicitor.balance) / float(price.last)
#
#        slots = {}
#        slots['htmlPaymentAddress'] = str(self.lender.bitcoinAddress) 
#        slots['htmlAvailableBalanceFiat'] = str(self.solicitor.balance) 
#        slots['htmlLoanBalanceFiat'] = str(self.lender.balance) 
#
#        slots['htmlAvailableBalanceBtc'] = str(solicitorBalanceBTC) 
#        slots['htmlLoanBalanceBtc'] = str(lenderBalanceBTC) 
#
#        slots['htmlNextPaymentDate'] = str(config.convertTimestamp(float(config.create_timestamp())))
#        slots['htmlReturnRate'] = str('0.85%') 
#        yield tag.clone().fillSlots(**slots)
#
#    @renderer
#    def transaction(self, request, tag):
#        transactions = db.query(Transaction).filter(Transaction.userId == self.session_user['id'])
#        transactions = transactions.filter(Transaction.status == 'complete')
#        transactions = transactions.order_by(Transaction.create_timestamp.desc())
#
#        for transaction in transactions: 
#            slots = {}
#            slots['htmlContractName'] = 'Contract #%s' % str(transaction.id)
#            slots['htmlContractUrl'] = '../files/contract-%s.pdf' % str(transaction.id)
#            yield tag.clone().fillSlots(**slots)
#

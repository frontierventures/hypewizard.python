#!/usr/bin/env python
from twisted.web.template import Element, renderer
from twisted.web.template import XMLString
from twisted.python .filepath import FilePath

from data import db
from data import Profile, User

import config
import math
import twitter_api


class Caption(Element):
    loader = XMLString('''
                       <div xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="caption" class="caption">
                       <t:slot name="text" />
                       </div>
                       ''')

    def __init__(self, text):
        self.text = text

    @renderer
    def caption(self, request, tag):
        return tag.fillSlots(text=self.text)


class Featured(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/elements/elementFeatured0.xml').getContent())


class Footer(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/elements/footer0.xml').getContent())


class Header(Element):
    def __init__(self, session_user):
        self.session_user = session_user
        if self.session_user['id'] == 0:
            self.loader = XMLString(FilePath('templates/elements/header0.xml').getContent())
        else:
            self.loader = XMLString(FilePath('templates/elements/header1.xml').getContent())

        if self.session_user['level'] == 0:
            self.loader = XMLString(FilePath('templates/elements/header2.xml').getContent())

        self.user = db.query(User).filter(User.id == session_user['id']).first()
        self.profile = db.query(Profile).filter(Profile.user_id == session_user['id']).first()

    @renderer
    def info(self, request, tag):
        slots = {}
        slots['email'] = self.user.email
        slots['available_balance'] = str(self.profile.available_balance)
        slots['reserved_balance'] = str(self.profile.reserved_balance)
        slots['twitter_name'] = self.profile.twitter_name
        return tag.fillSlots(**slots)

    @renderer
    def conversion(self, request, tag):
        currency = self.session_user['currency']
        price = db.query(Price).filter(Price.currency == currency).first()

        slots = {}
        slots['htmlCurrency'] = currency
        slots['htmlPriceFiat'] = '%.2f' % float(price.last)
        return tag.fillSlots(**slots)

    @renderer
    def offer_count(self, request, tag):
        slots = {}
        slots['count'] = str(self.profile.offer_count)
        return tag.fillSlots(**slots)

    @renderer
    def transaction_count(self, request, tag):
        slots = {}
        slots['count'] = str(self.profile.transaction_count)
        return tag.fillSlots(**slots)


class TwitterSummary(Element):
    def __init__(self, session_user):
        self.session_user = session_user
        self.loader = XMLString(FilePath('templates/elements/twitter_summary.xml').getContent())
        self.twitter_user = twitter_api.get_user(self.session_user['twitter_name'])

    @renderer
    def twitter_info(self, request, tag):
        slots = {}
        slots['name'] = str(self.twitter_user.name)
        slots['created_at'] = str(self.twitter_user.created_at)
        slots['statuses_count'] = str(self.twitter_user.statuses_count)
        slots['followers_count'] = str(self.twitter_user.followers_count)
        slots['market_score'] = str(0)
        #slots['status_text'] = status.text.encode('utf-8')
        yield tag.clone().fillSlots(**slots)


class Invite(Element):
    def __init__(self):
        self.loader = XMLString('''
                                <a href="../becomeAffiliate" xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">
                                <img src="../images/affiliate-banner-small.gif" style="margin-left: 35px;"/>
                                </a>
                                ''')


class Alert(Element):
    def __init__(self, session_response):
        self.session_response = session_response
        self.loader = XMLString(FilePath('templates/elements/alert.xml').getContent())

    @renderer
    def message(self, request, tag):
        session_response = self.session_response
        index = session_response['class']
        messageClass = ['alert alert-block',
                        'alert alert-error',
                        'alert alert-success',
                        'alert alert-info']
        slots = {}
        slots['htmlMessageClass'] = messageClass[index]
        slots['htmlMessageText'] = session_response['text']
        return tag.fillSlots(**slots)


class Options(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/elements/options0.xml').getContent())


class Pagination(Element):
    def __init__(self, session_user, sessionSearch):
        self.sessionSearch = sessionSearch
        self.session_user = session_user
        self.loader = XMLString(FilePath('templates/elements/pagination.xml').getContent())

    @renderer
    def first(self, request, tag):
        sessionSearch = self.sessionSearch
        session_user = self.session_user

        slots = {}
        slots['htmlPageUrl'] = '../%s?goto=first' % session_user['page']
        if sessionSearch['sort'] == 'new':
            slots['htmlPageUrl'] = '../%s?sort=new&goto=first' % session_user['page']
        yield tag.clone().fillSlots(**slots)

    @renderer
    def previous(self, request, tag):
        sessionSearch = self.sessionSearch
        session_user = self.session_user

        slots = {}
        slots['htmlPageUrl'] = '../%s?goto=previous' % session_user['page']
        if sessionSearch['sort'] == 'new':
            slots['htmlPageUrl'] = '../%s?sort=new&goto=previous' % session_user['page']
        yield tag.clone().fillSlots(**slots)

    @renderer
    def next(self, request, tag):
        sessionSearch = self.sessionSearch
        session_user = self.session_user

        slots = {}
        slots['htmlPageUrl'] = '../%s?goto=next' % session_user['page']
        if sessionSearch['sort'] == 'new':
            slots['htmlPageUrl'] = '../%s?sort=new&goto=next' % session_user['page']
        yield tag.clone().fillSlots(**slots)

    @renderer
    def last(self, request, tag):
        sessionSearch = self.sessionSearch
        session_user = self.session_user

        slots = {}
        slots['htmlPageUrl'] = '../%s?goto=last' % session_user['page']
        if sessionSearch['sort'] == 'new':
            slots['htmlPageUrl'] = '../%s?sort=new&goto=last' % session_user['page']
        yield tag.clone().fillSlots(**slots)

    @renderer
    def link(self, request, tag):
        sessionSearch = self.sessionSearch
        session_user = self.session_user

        index = sessionSearch['index']
        productCount = sessionSearch['productCount']
        productsPerPage = sessionSearch['productsPerPage']
        #numberOfPages = productCount / productsPerPage
        lastPageIndex = math.ceil(float(productCount) / sessionSearch['productsPerPage'])
        lastPageIndex = int(lastPageIndex)
        print
        print
        print lastPageIndex

        startButton = 1
        endButton = startButton + lastPageIndex

        if lastPageIndex > 10:
            startButton = 1
            endButton = startButton + 10

            if index >= 5:
                startButton = index - 5
                endButton = startButton + 10

            if (lastPageIndex - index) < 5:
                startButton = lastPageIndex - 9
                endButton = startButton + 10

        #numberOfButtons = numberOfPages + 1

        for pageNumber in range(startButton, endButton):
            thisTagShouldBeActive = False

            if pageNumber == index:
                thisTagShouldBeActive = True

            slots = {}
            slots['htmlPageUrl'] = '../%s?index=%s' % (session_user['page'], pageNumber)
            if sessionSearch['sort'] == 'new':
                slots['htmlPageUrl'] = '../%s?sort=new&index=%s' % (session_user['page'], pageNumber)

            slots['htmlPageNumber'] = str(pageNumber)
            if thisTagShouldBeActive:
                slots['htmlClass'] = 'active'
            else:
                slots['htmlClass'] = ''
            yield tag.clone().fillSlots(**slots)


class ServerDownPage(Element):
    session_user = {}
    sessionSearch = {}

    def __init__(self, pageTitle):
        self.pageTitle = pageTitle
        self.loader = XMLString(FilePath('templates/elements/pages/serverDown2.xml').getContent())
        self.loader = XMLString(FilePath('templates/elements/pages/serverDown1.xml').getContent())

    @renderer
    def title(self, request, tag):
        slots = {}
        slots['htmlPageTitle'] = self.pageTitle
        return tag.fillSlots(**slots)


class TabCell(Element):
    loader = XMLString('''
                        <li xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="tab">
                        <a>
                        <t:attr name="class"><t:slot name="htmlClass" /></t:attr>
                        <t:attr name="href"><t:slot name="htmlUrl" /></t:attr>
                        <i>
                        <t:attr name="class"><t:slot name="htmlIcon" /></t:attr>
                        </i>
                        <t:slot name="htmlCaption" />
                        </a>
                        </li>
                        ''')

    def __init__(self, session_user, tabIndex):
        self.session_user = session_user
        self.tabIndex = tabIndex

    @renderer
    def tab(self, request, tag):
        session_user = self.session_user
        profile = db.query(Profile).filter(Profile.user_id == session_user['id']).first()
        store = db.query(StoreDirectory).filter(StoreDirectory.owner_id == session_user['id']).first()

        tabs = {}
        tabs[config.create_timestamp()] = ['../%s' % store.name, 'iside mprod', 'Products']
        tabs[config.create_timestamp()] = ['../orders?type=buy', 'iside mbuy', 'Buy Orders (%s)' % profile.buy_order_count]
        tabs[config.create_timestamp()] = ['../orders?type=sell', 'iside msell', 'Sell Orders (%s)' % profile.sell_order_count]
        tabs[config.create_timestamp()] = ['../inbox', 'iside minbox', 'Messages (%s)' % profile.unread_count]
        tabs[config.create_timestamp()] = ['../settings', 'iside msettings', 'Settings']

        if session_user['is_affiliate'] == 1:
            tabs[config.create_timestamp()] = ['../affiliateLinks', 'iside mprod', 'Affiliate']

        for index, key in enumerate(sorted(tabs.keys())):
            slots = {}

            slots['htmlClass'] = ''
            if index == self.tabIndex:
                slots['htmlClass'] = 'active'

            slots['htmlUrl'] = tabs[key][0]
            slots['htmlIcon'] = tabs[key][1]
            slots['htmlCaption'] = tabs[key][2]
            yield tag.clone().fillSlots(**slots)

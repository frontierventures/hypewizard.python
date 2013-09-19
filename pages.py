#!/usr/bin/env python
from twisted.web.template import Element, renderer, XMLString
from twisted.python.filepath import FilePath

import account
import ask
import bid
import elements
import faq
import forms
import market
import orders
import popups
import transactions


class Page(Element):
    session_user = {}

    def __init__(self, pageTitle, template):
        self.pageTitle = pageTitle
        self.loader = XMLString(FilePath(templates[template]).getContent())

    @renderer
    def title(self, request, tag):
        slots = {}
        slots['htmlPageTitle'] = self.pageTitle
        return tag.fillSlots(**slots)

    @renderer
    def header(self, request, tag):
        return elements.Header(self.session_user)

    @renderer
    def footer(self, request, tag):
        return elements.Footer()


class Account(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def twitter_summary(self, request, tag):
        return elements.TwitterSummary(self.session_user)

    @renderer
    def details(self, request, tag):
        return account.Details(self.session_user)


class Ask(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle
        self.filters = filters

    @renderer
    def details(self, request, tag):
        return ask.Details(self.session_user, self.filters)

    @renderer
    def twitter_summary(self, request, tag):
        return elements.TwitterSummary(self.session_user)

    @renderer
    def create_ask_popup(self, request, tag):
        return popups.CreateAsk(self.session_user)


class Bid(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle
        self.filters = filters

    @renderer
    def details(self, request, tag):
        return bid.Details(self.session_user, self.filters)

    @renderer
    def twitter_summary(self, request, tag):
        return elements.TwitterSummary(self.session_user)

    @renderer
    def create_bid_popup(self, request, tag):
        return popups.CreateBid()


class Campaign(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)


class Faq(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle
        self.filters = filters

    @renderer
    def details(self, request, tag):
        return faq.Details()


class Login(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def login_form(self, request, tag):
        return forms.Login(self.session_user, self.session_response)

    @renderer
    def recoverPasswordPopup(self, request, tag):
        return popups.RecoverPassword()


class Main(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)


class Market(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle
        self.filters = filters

    @renderer
    def orders(self, request, tag):
        return market.Market(self.session_user, self.filters)

    @renderer
    def create_ask_popup(self, request, tag):
        return popups.CreateAsk(self.session_user)

    @renderer
    def create_bid_popup(self, request, tag):
        return popups.CreateBid()

    @renderer
    def feature_disabled_popup(self, request, tag):
        return popups.FeatureDisabled()

    @renderer
    def engage_promoter_popup(self, request, tag):
        return popups.EngagePromoter(self.session_user)

    @renderer
    def engage_client_popup(self, request, tag):
        return popups.EngageClient(self.session_user)


class Orders(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    #@renderer
    #def orders(self, request, tag):
    #    return orders.Orders(self.session_user, self.filters)

    @renderer
    def create_order_popup(self, request, tag):
        return popups.CreateOrder()


class Register(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def registerForm(self, request, tag):
        return forms.Register(self.session_user, self.session_response)


class Transactions(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def transactions_table(self, request, tag):
        return transactions.Table(self.session_user, self.filters)


templates = {
        'account': 'templates/pages/account.xml',
        'ask': 'templates/pages/ask.xml',
        'bid': 'templates/pages/bid.xml',
        'campaign': 'templates/pages/campaign.xml',
        'faq': 'templates/pages/faq.xml',
        'home': 'templates/pages/home.xml',
        'login': 'templates/pages/login.xml',
        'market': 'templates/pages/market.xml',
        'orders': 'templates/pages/orders.xml',
        'register': 'templates/pages/register.xml',
        'transactions': 'templates/pages/transactions.xml'
    }

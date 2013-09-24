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
import offers
import orders
import popups
import terms
import transactions
import summary_asks
import summary_bids
import summary_orders
import summary_transactions
import summary_users


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
    def details(self, request, tag):
        return account.Details(self.session_user)

    @renderer
    def change_password_popup(self, request, tag):
        return popups.ChangePassword()

    @renderer
    def resend_token_popup(self, request, tag):
        return popups.ResendToken()

    @renderer
    def withdraw_popup(self, request, tag):
        return popups.Withdraw()


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
    def reset_password_popup(self, request, tag):
        return popups.ResetPassword()


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
        return market.Table(self.session_user, self.filters)

    @renderer
    def create_ask_popup(self, request, tag):
        return popups.CreateAsk(self.session_user)

    @renderer
    def create_bid_popup(self, request, tag):
        return popups.CreateBid()

    @renderer
    def deposit_popup(self, request, tag):
        return popups.Deposit()

    @renderer
    def feature_disabled_popup(self, request, tag):
        return popups.FeatureDisabled()

    @renderer
    def engage_promoter_popup(self, request, tag):
        return popups.EngagePromoter(self.session_user)

    @renderer
    def engage_client_popup(self, request, tag):
        return popups.EngageClient(self.session_user)

    @renderer
    def withdraw_ask_popup(self, request, tag):
        return popups.WithdrawAsk(self.session_user)

    @renderer
    def withdraw_bid_popup(self, request, tag):
        return popups.WithdrawBid(self.session_user)


class Offers(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def offers_table(self, request, tag):
        return offers.Table(self.session_user, self.filters)

    @renderer
    def approve_offer_popup(self, request, tag):
        return popups.ApproveOffer(self.session_user)

    @renderer
    def disapprove_offer_popup(self, request, tag):
        return popups.DisapproveOffer(self.session_user)


class Orders(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def orders_table(self, request, tag):
        return orders.Table(self.session_user, self.filters)


class Register(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def registerForm(self, request, tag):
        return forms.Register(self.session_user, self.session_response)


class Terms(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle
        self.filters = filters

    @renderer
    def details(self, request, tag):
        return terms.Details()


class Transactions(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def transactions_table(self, request, tag):
        return transactions.Table(self.session_user, self.filters)

    @renderer
    def claim_balance_popup(self, request, tag):
        return popups.ClaimBalance(self.session_user)


class SummaryAsks(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def asks_table(self, request, tag):
        return summary_asks.Table(self.session_user, self.filters)


class SummaryBids(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def bids_table(self, request, tag):
        return summary_bids.Table(self.session_user, self.filters)


class SummaryOrders(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def orders_table(self, request, tag):
        return summary_orders.Table(self.session_user, self.filters)


class SummaryTransactions(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def transactions_table(self, request, tag):
        return summary_transactions.Table(self.session_user, self.filters)


class SummaryUsers(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def users_table(self, request, tag):
        return summary_users.Table(self.session_user, self.filters)

    #@renderer
    #def approve_offer_popup(self, request, tag):
    #    return popups.ApproveOffer(self.session_user)

    #@renderer
    #def disapprove_offer_popup(self, request, tag):
    #    return popups.DisapproveOffer(self.session_user)


templates = {
        'account': 'templates/pages/account.xml',
        'ask': 'templates/pages/ask.xml',
        'bid': 'templates/pages/bid.xml',
        'campaign': 'templates/pages/campaign.xml',
        'faq': 'templates/pages/faq.xml',
        'home': 'templates/pages/home.xml',
        'login': 'templates/pages/login.xml',
        'market': 'templates/pages/market.xml',
        'offers': 'templates/pages/offers.xml',
        'orders': 'templates/pages/orders.xml',
        'register': 'templates/pages/register.xml',
        'terms': 'templates/pages/terms.xml',
        'transactions': 'templates/pages/transactions.xml',
        'summary_asks': 'templates/pages/summary_asks.xml',
        'summary_bids': 'templates/pages/summary_bids.xml',
        'summary_orders': 'templates/pages/summary_orders.xml',
        'summary_transactions': 'templates/pages/summary_transactions.xml',
        'summary_users': 'templates/pages/summary_users.xml'
    }

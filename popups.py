#!/usr/bin/env python
from twisted.web.template import Element, renderer
from twisted.web.template import XMLString
from twisted.python .filepath import FilePath

import config
import definitions

from data import db
import twitter_api


class ApproveTransaction(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['approve_transaction']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class ChangePassword(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['change_password']).getContent())


class ClaimBalance(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['claim_balance']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class CreateAsk(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['create_ask']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def campaign_type_option(self, request, tag):
        for key in definitions.campaign_types.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key
            slots['caption'] = definitions.campaign_types[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def niche_option(self, request, tag):
        for key in definitions.niches.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key
            slots['caption'] = definitions.niches[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def twitter_status_option(self, request, tag):
        twitter_statuses = twitter_api.get_statuses(self.session_user['twitter_name'])

        for twitter_status in twitter_statuses: 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = str(twitter_status.id)
            slots['caption'] =  twitter_status.text.encode('utf-8')
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class CreateBid(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['create_bid']).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def niche_option(self, request, tag):
        for key in definitions.niches.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key
            slots['caption'] = definitions.niches[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def campaign_type_option(self, request, tag):
        for key in definitions.campaign_types.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key
            slots['caption'] = definitions.campaign_types[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class Deposit(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['deposit']).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class DisapproveTransaction(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['disapprove_transaction']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class EngageClient(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['engage_client']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class EngagePromoter(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['engage_promoter']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def twitter_status_option(self, request, tag):
        twitter_statuses = twitter_api.get_statuses(self.session_user['twitter_name'])

        for twitter_status in twitter_statuses: 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = str(twitter_status.id)
            slots['caption'] =  twitter_status.text.encode('utf-8')
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class FeatureDisabled(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['feature_disabled']).getContent())


class ResendToken(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['resend_token']).getContent())

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class ResetPassword(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['reset_password']).getContent())


class Withdraw(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['withdraw']).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class WithdrawAsk(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['withdraw_ask']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


class WithdrawBid(Element):
    def __init__(self, session_user):
        self.loader = XMLString(FilePath(templates['withdraw_bid']).getContent())
        self.session_user = session_user

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)

    @renderer
    def is_confirmed_option(self, request, tag):
        choices = {
            'yes': 'Yes',
            'no': 'No'
            }

        for key in choices.keys(): 
            thisTagShouldBeSelected = False
            #if key == propertyStatus:
            #    thisTagShouldBeSelected = True

            slots = {}
            slots['value'] = key 
            slots['caption'] = choices[key] 
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag


templates = {
        'approve_transaction': 'templates/popups/approve_transaction.xml',
        'change_password': 'templates/popups/change_password.xml',
        'claim_balance': 'templates/popups/claim_balance.xml',
        'create_ask': 'templates/popups/create_ask.xml',
        'create_bid': 'templates/popups/create_bid.xml',
        'deposit': 'templates/popups/deposit.xml',
        'disapprove_transaction': 'templates/popups/disapprove_transaction.xml',
        'feature_disabled': 'templates/popups/feature_disabled.xml',
        'engage_client': 'templates/popups/engage_client.xml',
        'engage_promoter': 'templates/popups/engage_promoter.xml',
        'resend_token': 'templates/popups/resend_token.xml',
        'reset_password': 'templates/popups/reset_password.xml',
        'withdraw': 'templates/popups/withdraw.xml',
        'withdraw_ask': 'templates/popups/withdraw_ask.xml',
        'withdraw_bid': 'templates/popups/withdraw_bid.xml'
    }

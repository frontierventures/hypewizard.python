#!/usr/bin/env python
from twisted.web.template import Element, renderer
from twisted.web.template import XMLString
from twisted.python .filepath import FilePath

import config
import definitions

from data import db
import twitter_api


class CreateAsk(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['create_ask']).getContent())

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


class CreateBid(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['create_bid']).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        yield tag.clone().fillSlots(**slots)


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

    #@renderr
    #def form(self, request, tag):
    #    slots = {}
    #    yield tag.clone().fillSlots(**slots)


templates = {
        'create_ask': 'templates/popups/create_ask.xml',
        'create_bid': 'templates/popups/create_bid.xml',
        'feature_disabled': 'templates/popups/feature_disabled.xml',
        'engage_client': 'templates/popups/engage_client.xml',
        'engage_promoter': 'templates/popups/engage_promoter.xml'
    }

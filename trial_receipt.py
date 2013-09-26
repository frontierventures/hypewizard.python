#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python .filepath import FilePath

#from data import db
#from data import AffiliateLink, Order, Publisher, Store

import config
import pages

def assemble(root):
    root.putChild('receipt', Main())
    return root


class Page(Element):
    sessionUser = {}

    def __init__(self, pageTitle, template):
        self.pageTitle = pageTitle
        self.loader = XMLString(FilePath(templates[template]).getContent())

    @renderer
    def title(self, request, tag):
        slots = {}
        slots['htmlPageTitle'] = self.pageTitle
        return tag.fillSlots(**slots)


class Receipt(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)

    @renderer
    def receipt(self, request, tag):
         return ReceiptElement()
 

templates = {'receipt': 'templates/pages/receipt.xml'}

class Main(Resource):
    def render(self, request):
        #order = db.query(Order).filter(Order.id == orderId).first()
        Page = Receipt('', 'receipt')
        #print "%ssessionResponse: %s%s" % (config.color.YELLOW, sessionResponse, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class ReceiptElement(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/elements/receipt.xml').getContent())

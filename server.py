#!/usr/bin/env python
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.web.template import Element, renderer, renderElement, XMLString

import api
import ask
import account
import bid
import config
import faq
import login
import logout
import market
import offers
import orders
import pages
import pos
import register
import terms
import transactions
import summary_asks
import summary_bids
import summary_orders
import summary_transactions
import summary_users
import sys
from sessions import SessionManager


log.startLogging(sys.stdout)

root = market.Main()
root = market.assemble(root)
root = api.assemble(root)
root = ask.assemble(root)
root = account.assemble(root)
root = bid.assemble(root)
root = login.assemble(root)
root = offers.assemble(root)
root = orders.assemble(root)
root = pos.assemble(root)
root = register.assemble(root)
root = summary_asks.assemble(root)
root = summary_bids.assemble(root)
root = summary_orders.assemble(root)
root = summary_transactions.assemble(root)
root = summary_users.assemble(root)
root = transactions.assemble(root)

root.putChild('', root)
root.putChild('faq', faq.Main())
root.putChild('terms', terms.Main())
root.putChild('css', File('./css'))
root.putChild('js', File('./js'))
root.putChild('img', File('./img'))
root.putChild('ico', File('./ico'))
root.putChild('logout', logout.Main())

site = Site(root)

reactor.listenTCP(8180, site)
reactor.run()

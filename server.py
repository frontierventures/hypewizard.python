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
import pages
import register
import transactions
import sys
from sessions import SessionManager


log.startLogging(sys.stdout)

root = market.Main()
root = api.assemble(root)
root = ask.assemble(root)
root = account.assemble(root)
root = bid.assemble(root)
root = login.assemble(root)
root = offers.assemble(root)
root = register.assemble(root)
root = transactions.assemble(root)

root.putChild('', root)
root.putChild('faq', faq.Main())
root.putChild('css', File('./css'))
root.putChild('js', File('./js'))
root.putChild('img', File('./img'))
root.putChild('ico', File('./ico'))
root.putChild('logout', logout.Main())

site = Site(root)

reactor.listenTCP(8080, site)
reactor.run()

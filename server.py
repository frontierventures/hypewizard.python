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
import campaign
import config
import faq
import login
import logout
import market
import orders
import pages
import register
import sys
from sessions import SessionManager


log.startLogging(sys.stdout)

root = market.Main()
root = api.assemble(root)
root = ask.assemble(root)
root = account.assemble(root)
root = bid.assemble(root)
root = campaign.assemble(root)
root = login.assemble(root)
root = orders.assemble(root)
root = register.assemble(root)

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

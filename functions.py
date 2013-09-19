from twisted.web.resource import Resource
from sessions import SessionManager

from data import Profile, User
from data import db

import config
import decimal
import definitions
import inspect
import json

from decimal import ROUND_UP
D = decimal.Decimal


class SessionUser(Resource):
    def render(self, request):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        session_user = SessionManager(request).get_session_user()
        user = json.dumps(session_user)
        return user


class SessionShipping(Resource):
    def render(self, request):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        sessionProduct = SessionManager(request).getSessionProduct()
        try:
            shipping = json.dumps(sessionProduct['shipping'])
        except:
            shipping = json.dumps({'186': 0})
        return shipping


class ProductInfo(Resource):
    def render(self, request):
        productId = int(request.args.get('id')[0])
        product = db.query(View).filter(View.productId == productId).first()
        sessionProduct = {}
        sessionProduct['id'] = product.productId
        sessionProduct['timestamp'] = product.timestamp
        sessionProduct['count'] = product.count
        product = db.query(PhysicalProduct).filter(PhysicalProduct.id == productId).first()
        sessionProduct['name'] = product.name
        sessionProduct['imageCount'] = product.imageCount
        sessionProduct['imageHash'] = product.imageHash
        sessionProduct['sellerId'] = product.sellerId

        store = db.query(Store).filter(Store.ownerId == product.sellerId).first()
        sessionProduct['store'] = store.name

        sellerNote = db.query(SellerNote).filter(SellerNote.productId == productId).first()
        try:
            sessionProduct['note'] = sellerNote.text
        except:
            sessionProduct['note'] = ''

        product = json.dumps(sessionProduct)
        return product


class ProductShipping(Resource):
    def render(self, request):
        productId = int(request.args.get('id')[0])
        rates = db.query(Shipping).filter(Shipping.productId == productId)

        sessionShipping = {}
        for rate in rates:
            sessionShipping[rate.countryId] = rate.cost

        shipping = json.dumps(sessionShipping)
        return shipping


class LoadCountries(Resource):
    def render(self, request):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        countries = {}
        for index, country in enumerate(definitions.countries):
            countries[index] = country
        countries = json.dumps(countries)
        return countries


class LoadRating(Resource):
    def render(self, request):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        productId = int(request.args.get('id')[0])
        reviews = db.query(Review).filter(Review.productId == productId)
        #reviews = reviewData.get_By_ProductId(productId)

        total = 0
        count = reviews.count()
        for review in reviews:
            total += review.rating

        try:
            average = total / count
        except:
            average = 0

        rating = {}
        rating['count'] = count
        rating['average'] = average
        rating = json.dumps(rating)
        return rating


class LoadMessage(Resource):
    def render(self, request):

        messageId = int(request.args.get('id')[0])
        try:
            action = request.args.get('action')[0]
        except:
            action = ''

        message = db.query(Message).filter(Message.id == messageId).first()

        if action != 'reply' and message.status == 'unread':
            profile = db.query(Profile).filter(Profile.userId == message.receiverId).first()
            message.status = 'read'
            profile.unreadCount -= 1
            db.commit()

        sessionMessage = {}
        sessionMessage['timestamp'] = str(message.timestamp)
        sessionMessage['receiverId'] = str(message.receiverId)
        sessionMessage['senderId'] = str(message.senderId)
        sessionMessage['senderName'] = str(message.name)
        sessionMessage['subject'] = str(message.subject)
        sessionMessage['body'] = str(message.body)
        message = json.dumps(sessionMessage)
        return message


class LoadOrder(Resource):
    def render(self, request):

        orderId = int(request.args.get('id')[0])
        order = db.query(Order).filter(Order.id == orderId).first()
        sessionOrder = {}
        sessionOrder['sellerId'] = str(order.sellerId)
        sessionOrder['buyerId'] = str(order.buyerId)
        order = json.dumps(sessionOrder)
        return order


class LoadStore(Resource):
    def render(self, request):

        ownerId = int(request.args.get('ownerId')[0])
        store = db.query(Store).filter(Store.ownerId == ownerId).first()

        sessionStore = {}
        sessionStore['ownerId'] = str(ownerId)
        sessionStore['name'] = str(store.name)
        sessionStore['logo'] = str(store.logo)
        sessionStore['rank'] = str(store.rank)
        sessionStore['productCount'] = str(store.productCount)
        store = json.dumps(sessionStore)
        return store


def calculate(last, price):
    last = D(last)
    price = D(price)

    price = D(price / last)
    price = price.quantize(D('0.00000001'), rounding=ROUND_UP)
    return price


import collections


class Grouper(object):
    def __init__(self):
        self.counter = collections.Counter()

    def __call__(self, x):
        #print x
        x = x[1]
        self.counter[x] += 1
        return self.counter[x], x


def group(L, n):
    for i in range(0, len(L), n):
        val = L[i:i + n]
        yield tuple(val)

#if __name__ == "__main__":
#    L = [1, 2, 1, 4, 2, 4, 2, 1, 2, 2, 4, 4, 3, 1, 3, 2, 3, 1]

#    body = sorted(L, key=Grouper())
#    body = list(group(body, 4))
#    print body

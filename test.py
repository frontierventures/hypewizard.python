from twisted.trial import unittest
from twisted_web_test_utils import DummySite

class WebTest(unittest.TestCase):
    def setUp(self):
        self.web = DummySite(MainPage())

    @inlineCallbacks
    def test_get(self):
        response = yield self.web.get("childpage")
        self.assertEqual(response.value(), "hello")

    # if you have params / headers:
    response = yield self.web.get("childpage", {'paramone': 'value'}, {'referer': "http://somesite.com"})

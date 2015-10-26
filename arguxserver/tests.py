import unittest

from pyramid import testing
from pyramid import request


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_rest_view(self):
        from .views import MainViews
        #request = testing.DummyRequest(params={'host':'a','items':'b'},path='/argux/rest/1.0/host/a')
        r = request.Request.blank(path='/argux/rest/1.0/a/b')
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = MainViews(r)
        info = v.item_details()
        #self.assertEqual(info['fqdn'], 'a')

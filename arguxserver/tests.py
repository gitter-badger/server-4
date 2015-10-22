import unittest

from pyramid import testing
from pyramid import request


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_rest_view(self):
        from .views import RestViews
        #request = testing.DummyRequest(params={'host':'a','items':'b'},path='/argux/rest/1.0/host/a')
        r = request.Request.blank(path='/argux/rest/1.0/a/b')
        r.matchdict = {'host':'a','item':'b'}
        v = RestViews(r)
        info = v.items()
        self.assertEqual(info['fqdn'], 'a')

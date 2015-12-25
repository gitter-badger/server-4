import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from tests.mock import dao

from arguxserver.rest.views.item import RestItemViews

class RestTriggerViewsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @unittest.skip('not implemented')
    def test_hosts(self):
        """

        """
        r = request.Request.blank(path='/rest/1.0/item')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.DAO()
        v = RestItemViews(r)
        response = v.item_1_view()

        self.assertEquals(host['name'], "localhost")

    def test_triggers():
        return

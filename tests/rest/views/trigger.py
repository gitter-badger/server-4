import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from tests.mock import dao

from argux_server.rest.views.item import RestItemViews

from argux_server.util import (
    TRIGGER_EXPR
)

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

    @unittest.skip('not implemented')
    def test_triggers(self):
        return

    def test_trigger_regexp(self):
        ret = TRIGGER_EXPR.match("last() > 0")
        self.assertNotEqual(ret, None)
        self.assertEqual(ret.group(1), "last")
        self.assertEqual(ret.group(2), "")
        self.assertEqual(ret.group(3), ">")
        self.assertEqual(ret.group(4), "0")

        ret = TRIGGER_EXPR.match("last() > 0.0")
        self.assertNotEqual(ret, None)
        self.assertEqual(ret.group(1), "last")
        self.assertEqual(ret.group(2), "")
        self.assertEqual(ret.group(3), ">")
        self.assertEqual(ret.group(4), "0.0")

        ret = TRIGGER_EXPR.match("last() > 10")
        self.assertNotEqual(ret, None)
        self.assertEqual(ret.group(1), "last")
        self.assertEqual(ret.group(2), "")
        self.assertEqual(ret.group(3), ">")
        self.assertEqual(ret.group(4), "10")

import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from tests.mock import dao

from argux_server.rest.views.host import RestHostViews

class RestHostViewsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hosts(self):
        """

        """
        r = request.Request.blank(path='/argux/rest/1.0/host')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.DAO()
        v = RestHostViews(r)
        response = v.hosts_1_view()

        # Check if 'hosts' is part of the response
        self.assertEquals(('hosts' in response), True)

        # Check if hosts contains one member
        hosts = response['hosts']
        self.assertEquals(len(hosts), 1)

        # Check if the member is localhost
        host = hosts[0]
        self.assertEquals(host['name'], "localhost")

    def test_read_host(self):
        r = request.Request.blank(path='/argux/rest/1.0/host/localhost')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.DAO()
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = RestHostViews(r)
        response = v.host_1_view_get('localhost')

        # Check if 'name' is part of the response
        self.assertEquals(('name' in response), True)

        # Check if 'items' is part of the response
        self.assertEquals(('items' in response), True)

        # Check if 'details' is part of the response
        self.assertEquals(('details' in response), True)

        # Check if the correct hostname is returned
        self.assertEqual(response['name'], 'localhost')

        # Check if the nr of items is 0
        self.assertEqual(len(response['items']), 0)

        # Check if the nr of details is 0
        self.assertEqual(len(response['details']), 0)

    def test_read_host_with_items(self):
        r = request.Request.blank(path='/argux/rest/1.0/host/localhost?items=true')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.DAO()
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = RestHostViews(r)
        response = v.host_1_view_get('localhost')

        # Check if 'name' is part of the response
        self.assertEquals(('name' in response), True)

        # Check if 'items' is part of the response
        self.assertEquals(('items' in response), True)

        # Check if 'details' is part of the response
        self.assertEquals(('details' in response), True)

        # Check if the correct hostname is returned
        self.assertEqual(response['name'], 'localhost')

        # Check if the nr of items is 1
        self.assertEqual(len(response['items']), 1)

        # Check if the nr of details is 0
        self.assertEqual(len(response['details']), 0)

        # Check the contents of the items.
        items = response['items']
        self.assertEqual(items[0]['name'], 'CPU Load Average')
        self.assertEqual(items[0]['key'], 'cpu.load.avg[1]')
        self.assertEqual(items[0]['last_val'], '42')

    def test_create_host(self):
        r = request.Request.blank(path='/argux/rest/1.0/host/localhost', POST="TEST")
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.DAO()
        r.matchdict = {'host':'localhost'}
        v = RestHostViews(r)
        response = v.host_1_view_post('localhost')

        self.assertEquals(response.status_int, 201)

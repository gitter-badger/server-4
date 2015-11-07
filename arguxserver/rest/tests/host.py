import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from arguxserver import dao

from arguxserver.rest.views.host import RestHostViews

class RestHostViewsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hosts(self):
        r = request.Request.blank(path='/argux/rest/1.0/host')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.mock
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = RestHostViews(r)
        info = v.hosts()

    def test_read_host(self):
        r = request.Request.blank(path='/argux/rest/1.0/host/localhost')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.mock
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = RestHostViews(r)
        info = v.host_1_view()

    def test_read_host_with_items(self):
        r = request.Request.blank(path='/argux/rest/1.0/host/localhost?items=true')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.mock
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = RestHostViews(r)
        info = v.host_1_view()

    def test_create_host(self):
        r = request.Request.blank(path='/argux/rest/1.0/host/localhost', POST="TEST")
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.mock
        r.matchdict = {'host':'localhost','item':'NONE'}
        v = RestHostViews(r)
        info = v.host_1_view()

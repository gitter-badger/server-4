from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
    )

from arguxserver import models

@view_defaults(renderer='templates/home.pt')
class MainViews:

    def __init__(self, request):
        self.request = request
        self.dao = request.registry.settings['dao']

    # TODO
    @view_config(route_name='home')
    def home(self):
        return {"project":"A"}

    # TODO
    @view_config(route_name='hosts')
    def hosts(self):
        return {"project":"A"}


    @view_config(route_name='host', renderer='templates/host.pt')
    def host(self):
        host = self.request.matchdict['host']
        host_desc = ''
        h = self.dao.HostDAO.getHostByName(host)

        if (h):
            host_desc = h.description

        has_summary = False

        if (has_summary == True):
            action = 'summary'
        else:
            action = 'metrics'

        return {"argux_host": host, "argux_host_desc": host_desc, "action": action}

    @view_config(route_name='host_details', renderer='templates/host.pt')
    def host_details(self):
        host = self.request.matchdict['host']
        action = self.request.matchdict['action']

        host_desc = ''
        h = self.dao.HostDAO.getHostByName(host)

        if (h):
            host_desc = h.description

        return {"argux_host": host, "argux_host_desc": host_desc, "action": action}

    @view_config(route_name='item_details', renderer='templates/item_details.pt')
    def item_details(self):
        host = self.request.matchdict['host']
        item = self.request.matchdict['item']
        return {"argux_host": host, "argux_item": item}

    @view_config(route_name='dashboards', renderer='templates/dashboard.pt')
    def dashboard(self):
        return {"project":"A"}

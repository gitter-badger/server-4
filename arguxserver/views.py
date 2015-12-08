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

    @view_config(route_name='item', renderer='templates/item.pt')
    def item(self):
        host_name = self.request.matchdict['host']
        item_key  = self.request.matchdict['item']

        details = [
            {"name": "MAX", "ts": "1-1-1970", "value":"14" }
            ]

        host     = self.dao.HostDAO.getHostByName(host_name)
        item     = self.dao.ItemDAO.getItemByHostKey(host, item_key)
        return {
            "argux_host": host_name,
            "argux_item": item,
            "timespan_start": "-45m",
            "timespan_end": "now",
            "action": 'details',
            "item_details": details}

    @view_config(route_name='item_details', renderer='templates/item.pt')
    def item_details(self):
        host_name = self.request.matchdict['host']
        item_key  = self.request.matchdict['item']
        action    = self.request.matchdict['action']

        ts        = self.request.params.get('timespan', '30m')

        details = [
            {"name": "MAX", "ts": "1-1-1970", "value":"14" }
            ]

        host     = self.dao.HostDAO.getHostByName(host_name)
        item     = self.dao.ItemDAO.getItemByHostKey(host, item_key)

        a = self.dao.ItemDAO.getAlerts(item)

        n_alerts = len(a)

        return {
            "argux_host": host_name,
            "argux_item": item,
            "timespan_start": "-40m",
            "timespan_end": "now",
            "action": action,
            'active_alerts': n_alerts,
            "item_details": details}

    @view_config(route_name='dashboards', renderer='templates/dashboard.pt')
    def dashboard(self):
        return {"project":"A"}

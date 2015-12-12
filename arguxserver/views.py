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
        n_alerts = 0
        h = self.dao.HostDAO.get_host_by_name(host)

        if (h):
            host_desc = h.description

        has_summary = False

        if (has_summary == True):
            action = 'summary'
        else:
            action = 'metrics'

        return {
            "argux_host": host,
            "argux_host_desc": host_desc,
            "active_alerts": n_alerts,
            "action": action}

    @view_config(route_name='host_details', renderer='templates/host.pt')
    def host_details(self):
        host = self.request.matchdict['host']
        action = self.request.matchdict['action']
        n_alerts = 0

        host_desc = ''
        h = self.dao.HostDAO.get_host_by_name(host)

        if (h):
            host_desc = h.description

        return {
            "argux_host": host,
            "argux_host_desc": host_desc,
            "active_alerts": n_alerts,
            "action": action}

    @view_config(route_name='item', renderer='templates/item.pt')
    def item(self):
        self.request.matchdict['action'] = 'details'

        return self.item_details()

    @view_config(route_name='item_details', renderer='templates/item.pt')
    def item_details(self):
        host_name = self.request.matchdict['host']
        item_key  = self.request.matchdict['item']
        action    = self.request.matchdict['action']

        ts        = self.request.params.get('timespan', '30m')

        details = [
            {"name": "MAX", "ts": "1-1-1970", "value":"14" }
            ]

        host     = self.dao.HostDAO.get_host_by_name(host_name)
        item     = self.dao.ItemDAO.get_item_by_host_key(host, item_key)

        a = self.dao.ItemDAO.get_alerts(item)

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

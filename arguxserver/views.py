from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

@view_defaults(renderer='templates/home.pt')
class MainViews:

    def __init__(self, request):
        self.request = request

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
        return {"argux_host": host}

    @view_config(route_name='host_details', renderer='templates/host_details.pt')
    def host_details(self):
        host = self.request.matchdict['host']
        return {"argux_host": host}

    @view_config(route_name='item_details', renderer='templates/item_details.pt')
    def item_details(self):
        host = self.request.matchdict['host']
        item = self.request.matchdict['item']
        return {"argux_host": host, "argux_item": item}

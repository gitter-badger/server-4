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

    @view_config(route_name='home')
    def home(self):
        return {"project":"A"}

    @view_config(route_name='hosts')
    def hosts(self):
        return {"project":"A"}

    @view_config(route_name='host', renderer='templates/host.pt')
    def host(self):
        host = self.request.matchdict['host']
        return {"argux_host": host}

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPNotFound,
    HTTPFound
)

from pyramid.security import (
    remember,
    forget,
)

import json

from . import BaseView

class MonitorViews(BaseView):

    @view_config(
        route_name='monitor_default',
        renderer='templates/monitor.pt',
        permission='view'
    )
    def monitors_default(self):
        self.request.matchdict['action'] = 'icmp'

        return self.monitors()

    @view_config(
        route_name='monitor',
        renderer='templates/monitor.pt',
        permission='view'
    )
    def monitors(self):
        action = self.request.matchdict['action']
        hosts = []

        d_hosts = self.dao.host_dao.get_all_hosts()

        for host in d_hosts:
            hosts.append({'name': host.name})

        return {
            "hosts": hosts,
            "userid": self.request.authenticated_userid,
            "action": action}

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
            "action": action}

    @view_config(
        route_name='monitor_edit',
        renderer='templates/monitor_edit.pt',
        permission='view'
    )
    def monitor_edit(self):
        action = self.request.matchdict['action']
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address']

        domains = []
        hosts = []

        d_host = self.dao.host_dao.get_host_by_name(host_name)
        d_address = self.dao.host_dao.get_address(d_host, address)

        for monitor in d_address.monitors:
            for domain in monitor.domains:
                domains.append({
                    "domain": domain.domain,
                    "records": {
                        "A": domain.record_a,
                        "AAAA": domain.record_aaaa,
                        "MX": domain.record_mx
                    }
                })

        return {
            "host": host_name,
            "address": address,
            "action": action,
            "domains": domains
        }

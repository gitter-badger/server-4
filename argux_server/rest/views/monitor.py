"""RestView for Monitors."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.httpexceptions import (
    HTTPBadRequest
)


from pyramid.response import Response

import json

from . import RestView

from argux_server.monitors import MONITORS

@view_defaults(renderer='json')
class RestMonitorViews(RestView):

    """RestMonitor View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_monitor_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
    def monitor_1_view_create(self):
        monitor_type = self.request.matchdict['type'].upper()
        host_name = self.request.matchdict['host']
        address = self.request.matchdict['address']

        try:
            options = self.request.json_body.get('options', None)
        except ValueError:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing options'
                }))

        if not monitor_type in MONITORS:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'invalid type'
                }))

        monitor = MONITORS.get(monitor_type)

        if monitor.validate_options(options) == False:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'invalid options'
                }))

        d_host = self.dao.host_dao.get_host_by_name(
            name = host_name)
        if d_host is None:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing host'
                }))

        d_address = self.dao.host_dao.get_address(
            host=d_host,
            address=address)
        if d_address is None:
            raise HTTPBadRequest(
                body=json.dumps({
                    'error': '400 Bad Request',
                    'message': 'missing address'
                }))

        self.dao.monitor_dao.create_monitor(
            monitor_type,
            d_address,
            options)

        return {'ok':'ok'}

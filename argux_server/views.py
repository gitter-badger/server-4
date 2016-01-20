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
    authenticated_userid
)

from argux_server.util import (
    TIMESPAN_EXPR,
)

import json


@view_defaults(renderer='templates/host_overview.pt')
class MainViews:

    def __init__(self, request):
        self.request = request
        self.dao = request.registry.settings['dao']


    # pylint: disable=no-self-use
    @view_config(
        route_name='home',
        permission='view'
    )
    def home(self):
        return self.host_overview_default()

    # pylint: disable=no-self-use
    @view_config(
        route_name='host_overview_default',
        renderer='templates/host_overview.pt',
        permission='view',
    )
    def host_overview_default(self):
        return {
            "userid": authenticated_userid(self.request),
            "fs": False,
            "action": 'overview'}

    # pylint: disable=no-self-use
    @view_config(
        route_name='host_overview',
        renderer='templates/host_overview.pt',
        permission='view'
    )
    def host_overview(self):
        action = self.request.matchdict['action']
        return {
            "userid": authenticated_userid(self.request),
            "fs": False,
            "action": action}

    @view_config(
        route_name='host_default',
        renderer='templates/host.pt',
        permission='view'
    )
    def host_default(self):
        host_name = self.request.matchdict['host']
        host_desc = ''
        n_alerts = 0
        host = self.dao.host_dao.get_host_by_name(host_name)

        if host:
            host_desc = host.description

        has_summary = False

        if has_summary is True:
            action = 'summary'
        else:
            action = 'metrics'

        return {
            "argux_host": host_name,
            "argux_host_desc": host_desc,
            "userid": authenticated_userid(self.request),
            "fs": False,
            "active_alerts": n_alerts,
            "action": action}

    @view_config(
        route_name='host',
        renderer='templates/host.pt',
        permission='view'
    )
    def host(self):
        host = self.request.matchdict['host']
        action = self.request.matchdict['action']
        n_alerts = 0

        host_desc = ''
        h = self.dao.host_dao.get_host_by_name(host)

        if h:
            host_desc = h.description

        return {
            "argux_host": host,
            "argux_host_desc": host_desc,
            "userid": authenticated_userid(self.request),
            "fs": False,
            "active_alerts": n_alerts,
            "action": action}

    @view_config(
        route_name='item',
        renderer='templates/item.pt',
        permission='view'
    )
    def item(self):
        self.request.matchdict['action'] = 'details'

        return self.item_details()

    @view_config(
        route_name='item_details',
        renderer='templates/item.pt',
        permission='view'
    )
    def item_details(self):
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']
        action = self.request.matchdict['action']

        timespan = self.request.params.get('timespan', '30m')

        # Validate timespan input and default to 30 minutes
        # if it fails.
        i = TIMESPAN_EXPR.match(timespan)
        if i is None:
            timespan = '30m'
        
        has_details = False

        host = self.dao.host_dao.get_host_by_name(host_name)
        item = self.dao.item_dao.get_item_by_host_key(host, item_key)

        if item.itemtype.name == 'float':
            has_details = True

        alerts = self.dao.item_dao.get_alerts(item)

        return {
            "argux_host": host_name,
            "argux_item": item,
            "userid": authenticated_userid(self.request),
            "timespan": timespan,
            "action": action,
            "fs": False,
            'active_alerts': len(alerts),
            "has_details": has_details}

    @forbidden_view_config()
    def forbidden_view(self):
        if authenticated_userid(self.request):
            return HTTPForbidden()

        url = self.request.route_url(
            'login',
            _query=(('next', self.request.path),))
        return HTTPFound(location=url)

    @view_config(
        route_name='login',
        renderer='templates/login.pt',
    )
    def login_html(self):
        session = self.request.session
        if self.request.method == "POST":
            username = self.request.params['username']
            password = self.request.params['password']

            if username == password:
                session['username'] = username

                headers = remember(self.request, username)

                url = self.request.route_url('home')

                response = HTTPFound(location=url)
                response.headerlist.extend(headers)

                return response
            return {}
        return {}

    @view_config(
        route_name='logout'
    )
    def logout(self):
        self.request.session.invalidate()

        headers = forget(self.request)
        url = self.request.route_url('home')

        response = HTTPFound(location=url)
        response.headerlist.extend(headers)

        return response

    @view_config(
        route_name='dashboards',
        renderer='templates/dashboard.pt',
        permission='view'
    )
    def dashboard(self):
        return {}

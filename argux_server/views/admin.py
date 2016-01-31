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

from . import BaseView


class AdminViews(BaseView):

    # pylint: disable=no-self-use
    @view_config(
        route_name='admin',
        renderer='templates/admin.pt',
        permission='view'
    )
    def admin(self):
        return {
            "userid": authenticated_userid(self.request),
            "action": 'users'}

    # pylint: disable=no-self-use
    @view_config(
        route_name='admin_users',
        renderer='templates/admin.pt',
        permission='view',
    )
    def admin_users(self):
        return {
            "userid": authenticated_userid(self.request),
            "action": 'users'}

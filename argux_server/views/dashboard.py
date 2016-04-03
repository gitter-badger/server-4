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

class DashboardViews(BaseView):

    @view_config(
        route_name='dashboards',
        renderer='templates/dashboard.pt',
        permission='view'
    )
    def dashboards(self):
        return {"A":"A"}

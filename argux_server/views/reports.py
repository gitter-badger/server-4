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

class ReportsViews(BaseView):

    @view_config(
        route_name='reports_default',
        renderer='templates/reports.pt',
        permission='view'
    )
    def reports_default(self):
        return {"A":"A"}

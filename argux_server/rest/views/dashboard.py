"""RestView for dashboard-items."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from . import RestView


@view_defaults(renderer='json')
class RestDashboardViews(RestView):

    """Rest Dashboard views.

    Return stuff for charts/tables.
    """

    def chart_1_view(self):
        return {}

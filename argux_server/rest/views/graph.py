"""RestView for Graphs."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import dateutil.parser

from datetime import datetime, timedelta

import json

import math

from . import RestView

from argux_server.util import (
    TIME_OFFSET_EXPR,
    DATE_FMT
)


@view_defaults(renderer='json')
class RestGraphViews(RestView):

    """RestItemViews class.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_graph_1',
        request_method='GET',
        check_csrf=True,
        permission='view'
    )
    def graph_1_view_read(self):
        graph_id = self.request.matchdict['id']

        return {}

    @view_config(
        route_name='rest_graph_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
    def graph_1_view_update(self):
        graph_id = self.request.matchdict['id']

        return {} 

    @view_config(
        route_name='rest_graph_1',
        request_method='DELETE',
        check_csrf=True,
        permission='view'
    )
    def graph_1_view_delete(self):
        graph_id = self.request.matchdict['id']

        return {}

    @view_config(
        route_name='rest_graphs_1',
        request_method='GET',
        check_csrf=True,
        permission='view'
    )
    def graphs_1_view_read(self):
        graph_id = self.request.matchdict['id']

        graph = self.dao.graph_dao.get_graph(graph_id=graph_id)

        return {
            'id': graph.id,
            'name': graph.name
        }

    @view_config(
        route_name='rest_graphs_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
    def graphs_1_view_create(self):

        graph = self.dao.graph_dao.create_graph(name=graph_name)

        return {
            'id': graph.id,
            'name': graph.name
        }

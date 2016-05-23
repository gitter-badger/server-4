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
        items = []

        graph = self.dao.graph_dao.get_graph(graph_id=graph_id)
        d_items = self.dao.graph_do.get_items(graph)
        for d_item in d_items:
            items.append({
                'name': d_item.name,
                'key': d_item.key,
                'host': d_item.host.name
            })
        return {
            'id': graph.id,
            'name': graph.name,
            'items': items
        }

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
        return {}

    @view_config(
        route_name='rest_graphs_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
    def graphs_1_view_create(self):

        try:
            json_body = self.request.json_body
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        try:
            items = json_body.get('items', [])
        except ValueError:
            item = []

        try:
            graph_name = json_body.get('name', None)
        except ValueError as err:
            return Response(
                status='400 Bad Request',
                content_type='application/json')
        if graph_name is None:
            return Response(
                status='400 Bad Request',
                content_type='application/json')


        if items.count == 0:
            return Response(
                status='400 Bad Request',
                content_type='application/json')

        d_items = []

        for item in items:
            d_host = self.dao.host_dao.get_host_by_name(item['host'])
            if d_host is None:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            d_item = self.dao.item_dao.get_item_by_host_key(
                host=d_host,
                key=item['name'])
            if d_item is None:
                return Response(
                    status='400 Bad Request',
                    content_type='application/json')

            d_items.append(d_item)

        graph = self.dao.graph_dao.create_graph(name=graph_name)

        for d_item in d_items:
            self.dao.graph_dao.graph_add_item(graph, d_item)

        return {
            'id': graph.id,
            'name': graph.name,
            'items': items
        }

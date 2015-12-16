from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

from . import RestView

@view_defaults(renderer='json')
class RestHostViews(RestView):
    """
    
    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(route_name='rest_hosts_1')
    def hosts(self):
        h = self.dao.host_dao.get_all_hosts()

        if (h == None):
            return HTTPNotFound()

        hosts = []
        for a in h:
            hosts.append({"name": a.name, "val": 0})

        return { 'hosts': hosts }

    @view_config(
            route_name='rest_host_1',
            request_method='POST')
    def host_1_view_post(self):
        host = self.request.matchdict['host']

        description=None
        try:
            description = self.request.json_body.get('description', None)
        except ValueError:
            description = None

        self.dao.host_dao.create_host(name=host, description=description)
        return Response(
            status='201 Created',
            content_type='application/json')

    @view_config(
            route_name='rest_host_1',
            request_method='GET')
    def host_1_view_get(self):
        host = self.request.matchdict['host']
        has_details = self.request.params.get('details', 'false')
        has_items   = self.request.params.get('items', 'false')

        h = self.dao.host_dao.get_host_by_name(host)

        items  = []
        details = []

        if (h == None):
            return Response(
                status="404 Not Found",
                content_type='application/json',
                charset='utf-8',
                body='{"error":"NOT FOUND"}')

        if (has_items == 'true'):
            items = self._get_items(h)

        if (has_details == 'true'):
            details = []


        return {
            'name' : h.name,
            'items': items,
            'details': details
            }

    def _get_items(self, host):

        i = self.dao.item_dao.get_items_from_host(host)
        if (i == None):
            return []

        items = []
        for a in i:
            if (a.name):
                name = a.name.name
            else:
                name = None

            if (a.category):
                category = a.category.name
            else:
                category = None

            v = self.dao.item_dao.get_last_value(a)

            if (v):
                items.append({
                    "category": category,
                    "name": name,
                    "key": a.key,
                    "last_val": v.value,
                    "last_ts": v.timestamp.strftime("%Y-%m-%dT%H:%M:%S")})
            else:
                items.append({
                    "category": category,
                    "name": name,
                    "key": a.key })
        return items


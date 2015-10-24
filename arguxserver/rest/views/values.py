from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

from arguxserver.dao import (
    HostDAO,
    ItemDAO,
    ValuesDAO
    )

import dateutil.parser

@view_defaults(renderer='json')
class RestValuesViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='values_1')
    def values_1_view(self):

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if (self.request.method == "GET"):
            self.values_1_view_read(host, item)

        if (self.request.method == "POST"):
            self.values_1_view_create(host, item)

    def values_1_view_read(self, host, item):
        time = self.request.params.get('time', '60')
        start_time = self.request.params.get('start_time', '-1')
        end_time = self.request.params.get('end_time', '-1')
        return {'fqdn': host, 'item': item, 'time': time}

    def values_1_view_create(self, host, item):
        try:
            value = self.request.json_body.get('value', None)
            ts = self.request.json_body.get('timestamp', None)
        except ValueError:
            value= None
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "value not specified"}')

        h = HostDAO.getHostByName(host)
        i = ItemDAO.getItemByHostKey(h, item)

        t = dateutil.parser.parse(ts)

        ValuesDAO.pushValue(i, t, value)

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

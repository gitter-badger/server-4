from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

import dateutil.parser

from . import RestView

@view_defaults(renderer='json')
class RestValuesViews(RestView):

    @view_config(route_name='values_1')
    def values_1_view(self):

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if (self.request.method == "GET"):
            return self.values_1_view_read(host, item)

        if (self.request.method == "POST"):
            self.values_1_view_create(host, item)

    def values_1_view_create(self, host, item):
        dao = self.dao

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

        h = dao.HostDAO.getHostByName(host)
        i = dao.ItemDAO.getItemByHostKey(h, item)

        t = dateutil.parser.parse(ts)

        dao.ValuesDAO.pushValue(i, t, value)

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

    #
    # Read Values
    #
    def values_1_view_read(self, host, item):
        dao = self.dao

        values = []
        #query = self.request.json_body.get('query', None)
        query = self.request.params.get('query', None)
        show_date = self.request.params.get('show_date', 'true')

        if (query == None):
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "query not specified"}')

        if (show_date == 'false'):
            #date_fmt = "%Y-%m-%dT%H:%M:%S"
            date_fmt = "%m/%d/%Y %H:%M:%S"
        else:
            date_fmt = "%H:%M"

        h = dao.HostDAO.getHostByName(host)
        i = dao.ItemDAO.getItemByHostKey(h, item)

        v = dao.ValuesDAO.getValues(i)

        for value in v:
            values.append ( {
            'ts': value.timestamp.strftime(date_fmt),
            'value': value.value
            } )

        return {
                'host': host,
                'item': item,
                'values': values }


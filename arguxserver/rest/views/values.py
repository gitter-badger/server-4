from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

import dateutil.parser

from datetime import datetime, timedelta

from . import RestView

@view_defaults(renderer='json')
class RestValuesViews(RestView):
    """
    
    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
            route_name='rest_values_1',
            request_method='POST')
    def values_1_view_create(self):
        dao = self.dao

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']


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
    @view_config(
            route_name='rest_values_1',
            request_method='GET')
    def values_1_view_read(self):
        dao = self.dao

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        values = []
        q_start = self.request.params.get('start', '-30m')
        q_end = self.request.params.get('end', 'now')

        show_date = self.request.params.get('show_date', 'true')

        start = dateutil.parser.parse(q_start)

        if (q_end == 'now'):
            end = datetime.now()
            start = end - timedelta(minutes=30)
        elif (q_end == None):
            end = datetime.now()
        else:
            end = dateutil.parser.parse(q_end)
            start = end - timedelta(minutes=30)

        if (False):
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "query not specified"}')

        date_fmt = "%m/%d/%Y %H:%M:%S"

        h = dao.HostDAO.getHostByName(host)
        i = dao.ItemDAO.getItemByHostKey(h, item)

        v = dao.ValuesDAO.getValues(i, start_time = start, end_time = end)

        for value in v:
            values.append ( {
            'ts': value.timestamp.strftime(date_fmt),
            'value': value.value
            } )

        return {
                'host': host,
                'item': item,
                'values': values }


from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import dateutil.parser

from datetime import datetime, timedelta

import json

from . import RestView

from arguxserver.util import TIME_OFFSET_EXPR


@view_defaults(renderer='json')
class RestItemViews(RestView):

    """RestItemViews class.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(route_name='rest_item_1')
    def item_1_view(self):
        """Create Item or Return item.

        POST creates an Item.
        GET  returns Item Details.
        """
        # Fallback response
        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "dunno"}')

        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        if self.request.method == "POST":
            ret = self.item_1_view_create(host_name, item_key)

        if self.request.method == "GET":
            ret = self.item_details_1_view_read(host_name, item_key)

        return ret

    def item_1_view_create(self, host_name, item_key):
        dao = self.dao

        category = None

        try:
            item_name = self.request.json_body.get('name', None)
            item_desc = self.request.json_body.get('description', None)
            item_category = self.request.json_body.get('category', None)
            item_type_key = self.request.json_body.get('type', None)
        except ValueError:
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')

        if item_type_key is None:
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')

        host = dao.host_dao.get_host_by_name(host_name)
        if (item_name != None and item_desc != None):
            item_n = dao.item_dao.get_itemname_by_name(item_name)
            if item_n is None:
                item_n = dao.item_dao.create_itemname(item_name, item_desc)

        if not item_category is None:
            category = dao.item_dao.get_itemcategory_by_name(item_category)
            if category is None:
                category = dao.item_dao.create_itemcategory(item_category)

        item_type = dao.item_dao.get_itemtype_by_name(item_type_key)

        item = dao.item_dao.create_item(
            host,
            item_key,
            item_n,
            category,
            item_type)

        return Response(
            status='201 Created',
            content_type='application/json',
            charset='UTF-8',
            body=json.dumps({'name': item.key}))

    @view_config(route_name='rest_item_values_1',
                 request_method='POST')
    def item_values_1_view(self):
        dao = self.dao

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        try:
            value = self.request.json_body.get('value', None)
            ts = self.request.json_body.get('timestamp', None)
        except ValueError:
            value = None
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "value not specified"}')

        h = dao.host_dao.get_host_by_name(host)
        i = dao.item_dao.get_item_by_host_key(h, item)

        t = dateutil.parser.parse(ts)

        dao.item_dao.push_value(i, t, value)

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

    @view_config(route_name='rest_item_details_1')
    def item_details_1_view(self):

        # Fallback response
        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "don\'t do that"}')

        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        if self.request.method == "GET":
            ret = self.item_details_1_view_read(host_name, item_key)

        return ret

    def item_details_1_view_read(self, host_name, item_key):
        values = []
        alerts = []
        n_alerts = 0

        q_start = self.request.params.get('start', '-30m')
        q_end = self.request.params.get('end', 'now')

        get_values = self.request.params.get('get_values', 'true')
        get_alerts = self.request.params.get('get_alerts', 'false')

        i = self.ts_to_td(q_start)
        if not i is None:
            start_offset = i[0] * i[1]

        if q_end == 'now':
            end = datetime.now()
            start = end + start_offset
        elif q_end is None:
            end = datetime.now()
        else:
            end = dateutil.parser.parse(q_end)
            start = end - timedelta(minutes=30)

        if False:
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "query not specified"}')

        date_fmt = "%Y-%m-%dT%H:%M:%S"

        host = self.dao.host_dao.get_host_by_name(host_name)
        if host is None:
            return Response(
                status='404 Not Found',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps(
                    {
                        'error': 'Not Found',
                        'host': host_name
                    }))
                

        item = self.dao.item_dao.get_item_by_host_key(host, item_key)
        if item is None:
            return Response(
                status='404 Not Found',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps(
                    {
                        'error': 'Not Found',
                        'host': host_name,
                        'item': item_key 
                    }))

        if get_values:
            d_values = self.dao.item_dao.get_values(
                item,
                start_time = start,
                end_time = end)

            for value in d_values:
                values.append ( {
                'ts': value.timestamp.strftime(date_fmt),
                'value': value.value
                } )

        if get_alerts:
            d_alerts = self.dao.item_dao.get_alerts(item)
            n_alerts = len(d_alerts)

            for alert in d_alerts:
                alerts.append ( {
                'start_time': alert.start_time.strftime(date_fmt),
                'severity': alert.trigger.severity.key,
                'name': alert.trigger.name
                } )

        return {
                'host': host_name,
                'item': item_key,
                'active_alerts': n_alerts,
                'values': values,
                'alerts': alerts }

    def ts_to_td(self, ts):
        ret_s = 1
        ret_td = timedelta(minutes = 0)

        i = TIME_OFFSET_EXPR.match(ts)
        if i is None:
            return None

        # Check if it is a positive or negative return value
        if i.group(1) == '-':
            ret_s = -1

        # minutes?
        if i.group(3) == 'm':
            ret_td = timedelta(minutes = int(i.group(2)))

        # hours?
        if i.group(3) == 'h':
            ret_td = timedelta(hours = int(i.group(2)))

        return (ret_s, ret_td)

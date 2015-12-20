"""RestView for Items."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import dateutil.parser

from datetime import datetime, timedelta

import json

from . import RestView

from arguxserver.util import (
    TIME_OFFSET_EXPR,
    DATE_FMT
)


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
            ret = Response(
                status='404 Not Found',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps(
                    {
                        'error': 'Not Found',
                        'host': host_name,
                        'item': item_key
                    }))

            host = self.dao.host_dao.get_host_by_name(host_name)
            if host is not None:
                item = self.dao.item_dao.get_item_by_host_key(
                    host,
                    item_key)

                if item is not None:
                    ret = self.item_details_1_view_read(host, item)

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
        if item_name is not None and item_desc is not None:
            item_n = dao.item_dao.get_itemname_by_name(item_name)
            if item_n is None:
                item_n = dao.item_dao.create_itemname(item_name, item_desc)

        if item_category is not None:
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
            ret = Response(
                status='404 Not Found',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps(
                    {
                        'error': 'Not Found',
                        'host': host_name,
                        'item': item_key
                    }))

            host = self.dao.host_dao.get_host_by_name(host_name)
            if host is not None:
                item = self.dao.item_dao.get_item_by_host_key(
                    host,
                    item_key)

                if item is not None:
                    ret = self.item_details_1_view_read(host, item)

        return ret

    def item_details_1_view_read(self, host, item):
        values = []
        alerts = []

        q_start = self.request.params.get('start', None)
        q_end = self.request.params.get('end', 'now')

        get_values = self.request.params.get('get_values', 'true')
        get_alerts = self.request.params.get('get_alerts', 'false')


        if (q_start != None):
            start = dateutil.parser.parse(q_start)

        if q_end != 'now':
            end = dateutil.parser.parse(q_end)
        else:
            end = datetime.now()

        if get_values == 'true':
            values = self.__get_values(item, start, end)

        if get_alerts == 'true':
            active_alerts = self.__get_active_alerts(item)

        return {
            'host': host.name,
            'item': item.key,
            'active_alerts': len(active_alerts),
            'start_time': start.strftime(DATE_FMT),
            'end_time': end.strftime(DATE_FMT),
            'values': values,
            'alerts': active_alerts
        }

    def __get_active_alerts(self, item):
        """Return active alerts on an item."""
        alerts = []
        d_alerts = self.dao.item_dao.get_alerts(item)

        for alert in d_alerts:
            alerts.append({
                'start_time': alert.start_time.strftime(DATE_FMT),
                'severity': alert.trigger.severity.key,
                'acknowledgement': alert.acknowledgement,
                'name': alert.trigger.name
            })

        return alerts

    def __get_values(self, item, start, end):
        """Return array of timestamp+value objects within a timeframe.

        timestamp is formatted according to arguxserver.util.DATE_FMT

        This format should be in ISO8601 (YYYY/MM/DDTmm:hh:ssZ)
        """
        values = []
        d_values = self.dao.item_dao.get_values(
            item,
            start_time=start,
            end_time=end)

        for value in d_values:
            values.append({
                'ts': value.timestamp.strftime(DATE_FMT),
                'value': value.value
            })

        return values

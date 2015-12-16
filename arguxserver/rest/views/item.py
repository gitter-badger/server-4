from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import dateutil.parser

from datetime import datetime, timedelta

from . import RestView

from arguxserver.util import TIME_OFFSET_EXPR


@view_defaults(renderer='json')
class RestItemViews(RestView):

    """ RestItemViews class.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(route_name='rest_item_1')
    def item_1_view(self):

        # Fallback response
        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "dunno"}')

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if self.request.method == "GET":
            ret = self.item_1_view_read(host, item)

        if self.request.method == "POST":
            ret = self.item_1_view_create(host, item)

        return ret

    def item_1_view_read(self, host, item):
        time = self.request.params.get('time', '60')
        start_time = self.request.params.get('start_time', '-1')
        end_time = self.request.params.get('end_time', '-1')
        return {'fqdn': host, 'item': item, 'time': time}

    def item_1_view_create(self, host, item):
        dao = self.dao

        try:
            name = self.request.json_body.get('name', None)
            description = self.request.json_body.get('description', None)
            category = self.request.json_body.get('category', None)
            _type = self.request.json_body.get('type', None)
        except ValueError:
            name = None
            description = None
            category = None
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')

        if _type is None:
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')
        n = None
        c = None 

        h = dao.host_dao.get_host_by_name(host)
        if (name != None and description != None):
            n = dao.item_dao.get_itemname_by_name(name)
            if n is None:
                n = dao.item_dao.create_itemname(name, description)

        if not category is None:
            c = dao.item_dao.get_itemcategory_by_name(category)
            if c is None:
                c = dao.item_dao.create_itemcategory(category)

        t = dao.item_dao.get_itemtype_by_name(_type)

        i = dao.item_dao.create_item(h, item, n, c, t)
        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

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

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if self.request.method == "GET":
            ret = self.item_details_1_view_read(host, item)

        return ret

    def item_details_1_view_read(self, host, item):
        values = []
        alerts = []
        n_alerts = 0

        q_start = self.request.params.get('start', '-30m')
        q_end = self.request.params.get('end', 'now')

        get_values = self.request.params.get('get_values', 'true')
        get_alerts = self.request.params.get('get_alerts', 'false')

        i = self.ts_to_td(q_start)
        if not i is None:
             start_offset = i[0]*i[1]

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

        h = self.dao.host_dao.get_host_by_name(host)
        i = self.dao.item_dao.get_item_by_host_key(h, item)

        if get_values:
            v = self.dao.item_dao.get_values(i, start_time = start, end_time = end)
            for value in v:
                values.append ( {
                'ts': value.timestamp.strftime(date_fmt),
                'value': value.value
                } )
        if get_alerts:
            a = self.dao.item_dao.get_alerts(i)

            n_alerts = len(a)
            for alert in a:
                alerts.append ( {
                'start_time': alert.start_time.strftime(date_fmt),
                'severity': alert.trigger.severity.key,
                'name': alert.trigger.name
                } )

        return {
                'host': host,
                'item': item,
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

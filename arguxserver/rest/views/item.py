from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from . import RestView

@view_defaults(renderer='json')
class RestItemViews(RestView):
    """
    
    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(route_name='rest_item_1')
    def item_1_view(self):

        # Fallback response
        ret = Response(
            status='500 Internal Server Error',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "500 Internal Server Error", "message": "dunno"}')

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if (self.request.method == "GET"):
            ret = self.item_1_view_read(host, item)

        if (self.request.method == "POST"):
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

        if (_type == None):
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8',
                charset='UTF-8',
                body='{"error": "400 Bad Request", "message": "type not specified"}')
        n = None
        c = None 

        h = dao.HostDAO.getHostByName(host)
        if (name != None and description != None):
            n = dao.ItemNameDAO.getItemNameByName(name)
            if (n == None):
                n = dao.ItemNameDAO.createItemName(name, description)

        if (category != None):
            c = dao.ItemCategoryDAO.getItemCategoryByName(category)
            if (c == None):
                c = dao.ItemCategoryDAO.createItemCategory(category)

        t = dao.ItemTypeDAO.getItemTypeByName(_type)

        i = dao.ItemDAO.createItem(h, item, n, c, t)
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

        if (self.request.method == "GET"):
            ret = self.item_details_1_view_read(host, item)

        return ret

    def item_details_1_view_read(host, item):
        values = []
        alerts = []
        q_start = self.request.params.get('start', '-30m')
        q_end = self.request.params.get('end', 'now')

        get_values = self.request.params.get('get_values', 'true')
        get_alerts = self.request.params.get('get_alerts', 'false')

        i = self.ts_to_td(q_start)
        if (i != None):
             start_offset = i[0]*i[1]

        if (q_end == 'now'):
            end = datetime.now()
            start = end + start_offset
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

        date_fmt = "%d/%m/%Y %H:%M:%S"

        h = self.dao.HostDAO.getHostByName(host)
        i = self.dao.ItemDAO.getItemByHostKey(h, item)

        if get_values:
            v = self.dao.ItemDAO.getValues(i, start_time = start, end_time = end)
            for value in v:
                values.append ( {
                'ts': value.timestamp.strftime(date_fmt),
                'value': value.value
                } )

        return {
                'host': host,
                'item': item,
                'values': values,
                'active_alerts': alerts }

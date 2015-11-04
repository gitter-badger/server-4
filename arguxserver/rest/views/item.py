from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

@view_defaults(renderer='json')
class RestItemViews:
    def __init__(self, request):
        self.request = request
        self.dao = request.registry.settings['dao']

    @view_config(route_name='item_1')
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

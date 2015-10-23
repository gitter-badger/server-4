from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

@view_defaults(renderer='json')
class RestViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='hosts_1')
    def hosts(self):
        h = models.DBSession.query(models.Host)

        if (h == None):
            return HTTPNotFound()

        items = []
        for a in h:
            items.append(a.name)

        return { 'hosts': items }

    @view_config(route_name='host_1')
    def host(self):
        host  = self.request.matchdict['host']
        items = self.request.params.get('items', 'NONE')


        if (self.request.method == "GET"):
            h = models.DBSession.query(models.Host).filter(models.Host.name == host).first()

            if (h == None):
                return Response(
                    status="404 Not Found",
                    content_type='application/json',
                    charset='utf-8',
                    body='{"error":"NOT FOUND"}')

            i = models.DBSession.query(models.Item).filter(models.Item.host_id == h.id)

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

                items.append({
                    "category": category,
                    "name": name,
                    "key": a.key})

            return {
                'name' : h.name,
                'items': items
                }

        if (self.request.method == "POST"):
            h = models.Host(name=host)
            models.DBSession.add(h)
            return Response(
                status='201 Created',
                content_type='application/json')

        if (self.request.method == "PUT"):
            return {'fqdn':'PUT'}

    @view_config(route_name='item_1')
    def items(self):

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if (self.request.method == "GET"):
            time = self.request.params.get('time', '60')
            start_time = self.request.params.get('start_time', '-1')
            end_time = self.request.params.get('end_time', '-1')
            return {'fqdn': host, 'item': item, 'time': time}

        if (self.request.method == "POST"):
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
            h = models.DBSession.query(models.Host).filter(models.Host.name == host).first()
            if (name != None and description != None):
                n = models.DBSession.query(models.ItemName).filter(models.ItemName.name == name).first()
                if (n == None):
                    n = models.ItemName(name=name, description=description)

            if (category != None):
                c = models.DBSession.query(models.ItemCategory).filter(models.ItemCategory.name == category).first()
                if (c == None):
                    c = models.ItemCategory(name=category)

            t = models.DBSession.query(models.ItemType).filter(models.ItemType.name == _type).first()

            i = models.Item(host_id=h.id, key=item, name=n, category=c, itemtype=t)
            models.DBSession.add(i)
            return Response(
                status='201 Created',
                content_type='application/json; charset=UTF-8')

        if (self.request.method == "POST"):
            return {'fqdn':'POST'}


        return {'fqdn':'unknown'}

    @view_config(route_name='metric_1')
    def metrics(self):

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if (self.request.method == "GET"):
            time = self.request.params.get('time', '60')
            start_time = self.request.params.get('start_time', '-1')
            end_time = self.request.params.get('end_time', '-1')
            return {'fqdn': host, 'item': item, 'time': time}

        if (self.request.method == "POST"):
            try:
                value = self.request.json_body.get('value', None)
            except ValueError:
                value= None
                return Response(
                    status='400 Bad Request',
                    content_type='application/json',
                    charset='UTF-8',
                    body='{"error": "400 Bad Request", "message": "value not specified"}')

            h = models.DBSession.query(models.Host).filter(models.Host.name == host).first()
            i = models.DBSession.query(models.Item).filter(models.Item.host == h).filter(models.Item.key == item)
            return Response(
                status='201 Created',
                content_type='application/json; charset=UTF-8')

        if (self.request.method == "POST"):
            return {'fqdn':'POST'}

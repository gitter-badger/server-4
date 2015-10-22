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

    @notfound_view_config()
    def not_found(self):
        return Response('Not Found, dude', status='404 Not Found')
        

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
                return HTTPNotFound()

            i = models.DBSession.query(models.Item).filter(models.Item.host_id == h.id)

            items = []
            for a in i:
                if (a.name):
                    name = a.name.name
                else:
                    name = None

                items.append({
                    "name": name,
                    "key": a.key})

            return {
                'name' : h.name,
                'items': items
                }
        if (self.request.method == "POST"):
            return {'fqdn':'POST'}

        if (self.request.method == "PUT"):
            h = models.Host(name=host)
            models.DBSession.add(h)
            return Response(
                status='201 Created',
                content_type='application/json; charset=UTF-8')

    @view_config(route_name='item_1')
    def items(self):

        host = self.request.matchdict['host']
        item = self.request.matchdict['item']

        if (self.request.method == "GET"):
            time = self.request.params.get('time', '60')
            start_time = self.request.params.get('start_time', '-1')
            end_time = self.request.params.get('end_time', '-1')
            return {'fqdn': host, 'item': item, 'time': time}

        if (self.request.method == "PUT"):
            name = self.request.json_body['name']
            description = self.request.json_body['description']
            n = None

            h = models.DBSession.query(models.Host).filter(models.Host.name == host).first()
            if (name != None and description != None):
                n = models.DBSession.query(models.ItemName).filter(models.ItemName.name == name).first()
                if (n == None):
                    n = models.ItemName(name=name, description=description)
            i = models.Item(host_id=h.id, key=item, name=n)
            models.DBSession.add(i)
            return Response(
                status='201 Created',
                content_type='application/json; charset=UTF-8')

        if (self.request.method == "POST"):
            return {'fqdn':'POST'}


        return {'fqdn':'unknown'}

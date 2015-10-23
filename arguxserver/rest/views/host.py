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
    def host_1_view(self):

        # Fallback response
        ret = Response(
            status='500 Internal Server Error',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "500 Internal Server Error", "message": "dunno"}')

        host  = self.request.matchdict['host']
        items = self.request.params.get('items', 'NONE')

        if (self.request.method == "GET"):
            ret = self.host_1_view_read(host, items)

        if (self.request.method == "POST"):
            ret = self.host_1_view_create(host, items)

        return ret

    def host_1_view_read(self, host, items):
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

    def host_1_view_create(self, host, items):
        h = models.Host(name=host)
        models.DBSession.add(h)
        return Response(
            status='201 Created',
            content_type='application/json')

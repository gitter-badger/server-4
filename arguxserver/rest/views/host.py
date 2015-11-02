from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

from arguxserver.dao import (
    HostDAO,
    ItemDAO,
    ValuesDAO
    )

@view_defaults(renderer='json')
class RestViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='hosts_1')
    def hosts(self):
        h = models.DBSession.query(models.Host)

        if (h == None):
            return HTTPNotFound()

        hosts = []
        for a in h:
            hosts.append({"name": a.name, "val": 0})

        return { 'hosts': hosts }

    @view_config(route_name='host_1')
    def host_1_view(self):

        # Fallback response
        ret = Response(
            status='500 Internal Server Error',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "500 Internal Server Error", "message": "dunno"}')

        host    = self.request.matchdict['host']
        details = self.request.params.get('details', 'false')

        if (self.request.method == "GET"):
            ret = self.host_1_view_read(host, details)

        if (self.request.method == "POST"):
           ret = self.host_1_view_create(host)

        return ret

    def host_1_view_create(self, host):
        description=None
        try:
            description = self.request.json_body.get('description', None)
        except ValueError:
            description = None

        h = models.Host(name=host, description=description)
        models.DBSession.add(h)
        return Response(
            status='201 Created',
            content_type='application/json')

    def host_1_view_read(self, host, details):
        h = HostDAO.getHostByName(host)

        if (h == None):
            return Response(
                status="404 Not Found",
                content_type='application/json',
                charset='utf-8',
                body='{"error":"NOT FOUND"}')

        i = ItemDAO.getItemsFromHost(h)
        if (i == None):
            return Response(
                status="404 Not Found",
                content_type='application/json',
                charset='utf-8',
                body='{"error":"NOT FOUND"}')

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

            v = ValuesDAO.getLastValue(a)

            if (v):
                items.append({
                    "category": category,
                    "name": name,
                    "key": a.key,
                    "last_val": v.value,
                    "last_ts": v.timestamp.strftime("%Y-%m-%dT%H:%M:%S")})
            else:
                items.append({
                    "category": category,
                    "name": name,
                    "key": a.key })

        return {
            'name' : h.name,
            'items': items
            }


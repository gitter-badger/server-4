from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

@view_defaults(renderer='json')
class RestMetricViews:
    def __init__(self, request):
        self.request = request

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


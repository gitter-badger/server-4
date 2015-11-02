from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver.dao import (
    HostDAO,
    ItemCategoryDAO,
    ItemNameDAO,
    ItemTypeDAO,
    ItemDAO
    )

@view_defaults(renderer='json')
class RestHostDetailsViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='host_details_1')
    def host_details_1_view(self):

        # Fallback response
        ret = Response(
            status='500 Internal Server Error',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "500 Internal Server Error", "message": "dunno"}')

        host = self.request.matchdict['host']
        detail_id = self.request.matchdict['detail_id']

        if (self.request.method == "GET"):
            ret = self.host_details_1_view_read(host, detail_id)

        if (self.request.method == "POST"):
            ret = self.host_details_1_view_create(host, detail_id)

        return ret

    def host_details_1_view_read(self, host, detail_id):
        return {'fqdn': 'time'}

    def host_details_1_view_create(self, host, detail_id):
        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

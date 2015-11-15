from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from . import RestView

@view_defaults(renderer='json')
class RestHostDetailsViews(RestView):
    """
    
    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(route_name='rest_host_details_1')
    def host_details_1_view(self):

        # Fallback response
        ret = Response(
            status='500 Internal Server Error',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "500 Internal Server Error", "message": "dunno"}')

        host = self.request.matchdict['host']

        if (self.request.method == "GET"):
            ret = self.host_details_1_view_read(host)

        if (self.request.method == "POST"):
            ret = self.host_details_1_view_create(host)

        return ret

    def host_details_1_view_read(self, host):
        return {'fqdn': 'time'}

    def host_details_1_view_create(self, host):
        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

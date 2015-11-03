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
class RestNoteViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='note_1')
    def note_1_view(self):

        # Fallback response
        ret = Response(
            status='500 Internal Server Error',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "500 Internal Server Error", "message": "dunno"}')

        if (self.request.method == "GET"):
            ret = self.note_1_view_read()

        if (self.request.method == "POST"):
           ret = self.note_1_view_create()

        return ret

    def note_1_view_create(self):
        return Response(
            status='201 Created',
            content_type='application/json')

    def note_1_view_read(self):
        return Response(
            status='404 not found',
            content_type='application/json')


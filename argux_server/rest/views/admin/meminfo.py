"""RestView for Memory-Info."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from datetime import datetime

import json

from .. import RestView

import gc
import objgraph


@view_defaults(renderer='json')
class RestMemInfoViews(RestView):

    """RestNote views.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_admin_meminfo_1',
        check_csrf=True,
        permission='view'
    )
    def meminfo_1_view(self):
        gc.collect()

        #roots = objgraph.get_leaking_objects()
        #print(len(roots))
        #objgraph.show_most_common_types(objects=roots)
        objgraph.show_growth()
        
        objgraph.show_growth()
        return {'ok':'ok'}


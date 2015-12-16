from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

from arguxserver.util import TIME_OFFSET_EXPR

import dateutil.parser

from datetime import datetime, timedelta

from . import RestView

@view_defaults(renderer='json')
class RestTriggerViews(RestView):
    """
    
    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
            route_name='rest_triggers_1',
            request_method='POST')
    def trigger_1_view_create(self):
        dao     = self.dao
        host    = self.request.matchdict['host']
        item    = self.request.matchdict['item']
        name    = self.request.json_body.get('name', None)
        rule    = self.request.json_body.get('rule', None)
        description = self.request.json_body.get('description', None)

        h = dao.host_dao.get_host_by_name(host)
        i = dao.item_dao.get_item_by_host_key(h, item)

        try:
            t = dao.item_dao.create_trigger(i, name, rule, description)
        except Exception as e:
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8')

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

    #
    # Read Values
    #
    @view_config(
            route_name='rest_triggers_1',
            request_method='GET')
    def trigger_1_view_read(self):
        dao     = self.dao
        host    = self.request.matchdict['host']
        item    = self.request.matchdict['item']

        triggers = []

        h = dao.host_dao.get_host_by_name(host)
        i = dao.item_dao.get_item_by_host_key(h, item)

        t = dao.item_dao.get_triggers(i)
        for trigger in t:
            triggers.append( {
                'id':   trigger.id,
                'name': trigger.name,
                'rule': trigger.rule
            })

        return {
                'host':host,
                'item':item,
                'triggers': triggers }

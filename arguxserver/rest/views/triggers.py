"""Trigger REST Interface."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from . import RestView


@view_defaults(renderer='json')
class RestTriggerViews(RestView):

    """Views for REST interface configuring Triggers.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_triggers_1',
        request_method='POST')
    def trigger_1_view_create(self):
        """Create Trigger.

        Required Parameters:

          - Host
          - Item key
          - Trigger Name
          - Trigger Rule
          - Description
        """
        dao = self.dao
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']
        name = self.request.json_body.get('name', None)
        rule = self.request.json_body.get('rule', None)
        description = self.request.json_body.get('description', None)

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(h, item_key)

        try:
            trigger = dao.item_dao.create_trigger(
                item,
                name,
                rule,
                description)
        except Exception as e:
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8')

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

    @view_config(
        route_name='rest_triggers_1',
        request_method='GET')
    def trigger_1_view_read(self):
        """Get all triggers for an Item."""
        dao = self.dao
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        triggers = []

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(host, item_key)

        item_triggers = dao.item_dao.get_triggers(item)
        for trigger in item_triggers:
            triggers.append( {
                'id':   trigger.id,
                'name': trigger.name,
                'rule': trigger.rule
            })

        return {
                'host':host_name,
                'item':item_key,
                'triggers': triggers }

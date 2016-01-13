"""Trigger REST Interface."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

import json

from . import RestView

from arguxserver.util import (
    DATE_FMT
)


@view_defaults(renderer='json')
class RestTriggerViews(RestView):

    """Views for REST interface configuring Triggers.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
        route_name='rest_triggers_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
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
        severity    = self.request.json_body.get('severity', None)

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(host, item_key)

        trigger = None

        try:
            trigger = dao.item_dao.create_trigger(
                item,
                name,
                rule,
                description,
                severity)
        except ValueError as error:
            return Response(
                status='400 Bad Request',
                content_type='application/json',
                charset='UTF-8',
                body=json.dumps({'error': str(error)}))

        if trigger is None:
            return Response(
                status='500 Internal Server Error',
                content_type='application/json',
                charset='UTF-8')

        ret = {
            'name': trigger.name
        }

        return Response(
            status='201 Created',
            content_type='application/json',
            charset='UTF-8',
            body=json.dumps(ret))

    @view_config(
        route_name='rest_triggers_1',
        request_method='GET',
        check_csrf=True,
        permission='view'
    )
    def trigger_1_view_read(self):
        """Get all triggers for an Item."""
        dao = self.dao
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        triggers = []

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(host, item_key)

        item_triggers = dao.item_dao.get_triggers(item)

        active_alert_count = dao.item_dao.get_active_alert_count(item)

        for trigger in item_triggers:
            alert = dao.item_dao.get_last_alert_for_trigger(trigger)
            time = None

            if alert:
                if alert.end_time is not None:
                    time = alert.end_time.strftime(DATE_FMT)
                else:
                    time = 'now'
            else:
                time = None

            triggers.append({
                'id': trigger.id,
                'name': trigger.name,
                'rule': trigger.rule,
                'last_alert': time
            })

        return {
            'host': host_name,
            'item': item_key,
            'triggers': triggers,
            'active_alerts': active_alert_count
        }

    @view_config(
        route_name='rest_trigger_1',
        request_method='DELETE',
        check_csrf=True,
        permission='view'
    )
    def trigger_1_view_delete(self):
        """Get all triggers for an Item."""
        dao = self.dao
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']
        trigger_id = self.request.matchdict['id']

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(host, item_key)

        dao.item_dao.delete_trigger_by_id(item, trigger_id)
        return

    @view_config(
        route_name='rest_trigger_validate_1',
        request_method='POST',
        check_csrf=True,
        permission='view'
    )
    def trigger_1_validate(self):
        """Validate Trigger Rule."""
        dao = self.dao
        host_name = self.request.matchdict['host']
        item_key = self.request.matchdict['item']

        # trigger_name = self.request.json_body.get('name', None)
        trigger_rule = self.request.json_body.get('rule', None)

        host = dao.host_dao.get_host_by_name(host_name)
        item = dao.item_dao.get_item_by_host_key(host, item_key)

        ret = dao.item_dao.validate_trigger_rule(item, trigger_rule)

        return {
            'item': item.name.name,
            'valid': ret
        }

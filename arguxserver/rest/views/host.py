"""RestView for Hosts."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.response import Response

from . import RestView

from arguxserver.util import (
    TIME_OFFSET_EXPR,
    DATE_FMT
)


@view_defaults(renderer='json')
class RestHostViews(RestView):

    """RestHosts View.

    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(route_name='rest_hosts_1')
    def hosts_1_view(self):
        """Return array of all hosts."""
        d_hosts = self.dao.host_dao.get_all_hosts()

        hosts = []
        for host in d_hosts:
            hosts.append({"name": host.name, "val": 0})

        return {'hosts': hosts}

    @view_config(route_name='rest_host_1')
    def host_1_view(self):
        """Create host or return host.

        POST creates a host.
        GET  returns Host details.
        """
        host_name = self.request.matchdict['host']

        ret = Response(
            status='400 Bad Request',
            content_type='application/json',
            charset='UTF-8',
            body='{"error": "400 Bad Request", "message": "dunno"}')

        if self.request.method == "POST":
            ret = self.host_1_view_post(host_name)

        if self.request.method == "GET":
            ret = self.host_1_view_get(host_name)

        return ret

    def host_1_view_post(self, host_name):
        """Create new host."""
        description = None
        try:
            description = self.request.json_body.get('description', None)
        except ValueError:
            description = None

        self.dao.host_dao.create_host(
            name=host_name,
            description=description)

        return Response(
            status='201 Created',
            content_type='application/json')

    def host_1_view_get(self, host_name):
        """Return host details."""
        host_get_details = self.request.params.get('details', 'false')
        host_get_items = self.request.params.get('items', 'false')
        host_get_alerts = self.request.params.get('alerts', 'false')

        host = self.dao.host_dao.get_host_by_name(host_name)

        items = []
        details = []
        active_alerts = []

        if host is None:
            return Response(
                status="404 Not Found",
                content_type='application/json',
                charset='utf-8',
                body='{"error":"NOT FOUND"}')

        if host_get_items == 'true':
            items = self._get_items(host)

        if host_get_alerts == 'true':
            active_alerts = self.__get_active_alerts(host)

        if host_get_details == 'true':
            details = []


        return {
            'name' : host.name,
            'items': items,
            'details': details,
            'alerts': active_alerts,
            'active_alerts': len(active_alerts),
        }

    def __get_active_alerts(self, host):
        d_items = self.dao.item_dao.get_items_from_host(host)
        if (d_items == None):
            return []

        alerts = []
        for item in d_items:
            d_alerts = self.dao.item_dao.get_alerts(item)
            for alert in d_alerts:
                alerts.append({
                    'start_time': alert.start_time.strftime(DATE_FMT),
                    'severity': alert.trigger.severity.key,
                    'acknowledgement': alert.acknowledgement,
                    'name': alert.trigger.name,
                    'item': {
                        'key': alert.trigger.item.key,
                        'name': alert.trigger.item.name.name
                    }
                })

        return alerts

    def _get_items(self, host):
        """Get list of items for host."""
        d_items = self.dao.item_dao.get_items_from_host(host)
        if (d_items == None):
            return []

        items = []
        for item in d_items:
            if item.name:
                name = item.name.name
            else:
                name = None

            if item.category:
                category = item.category.name
            else:
                category = None

            value = self.dao.item_dao.get_last_value(item)

            if value:
                items.append({
                    "category": category,
                    "name": name,
                    "key": item.key,
                    "last_val": value.value,
                    "last_ts": value.timestamp.strftime("%Y-%m-%dT%H:%M:%S")})
            else:
                items.append({
                    "category": category,
                    "name": name,
                    "key": item.key})
        return items


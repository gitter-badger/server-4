"""Data Access Object class for handling Servers."""

from argux_server.models.Monitor import Monitor
from argux_server.models.MonitorType import MonitorType
from argux_server.models.MonitorOption import MonitorOption

from .BaseDAO import BaseDAO


class MonitorDAO(BaseDAO):

    """MonitorDAO class.

    Object for accessing Monitor objects.
    """

    def create_monitor(self, monitor_type, host_address, options):
        d_type = self.db_session.query(MonitorType)\
            .filter(MonitorType.name == monitor_type.upper())\
            .first()
        if d_type is None:
            raise KeyError

        monitor = Monitor(
            host_address = host_address,
            monitor_type = d_type)

        self.db_session.add(monitor)

        for key, value in options.items():
            option = MonitorOption(key=key, value=value, monitor=monitor)
            self.db_session.add(option)
        return

    def add_monitor_type(self, name):
        """Add a new monitor-type if it does not already exist."""
        monitor_type = self.db_session.query(MonitorType)\
            .filter(MonitorType.name == name)\
            .first()
        if monitor_type is None:
            monitor_type = MonitorType(
                name=name.upper())
            self.db_session.add(monitor_type)

    def get_all_monitors_for_type(self, monitor_type):
        """Query all monitors for a type."""
        monitors = self.db_session.query(Monitor)\
            .filter(Monitor.monitor_type_id == (
                self.db_session.query(MonitorType.id)\
                    .filter(MonitorType.name == monitor_type)
                )
            )\
            .all()

        return monitors

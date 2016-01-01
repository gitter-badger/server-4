"""Data Access Object class for handling Hosts."""

from arguxserver.models import (
    Host,
    Item,
    TriggerSeverity
)

from arguxserver.dao.util import (
    TRIGGER_CLASS,
    ALERT_CLASS
)

class HostDAO:

    """
    HostDAO Class.
    """

    def __init__(self, session):
        """Initialise HostDAO."""
        self.db_session = session

    def get_host_by_name(self, name):
        """Return host-object based on name."""
        host = self.db_session.query(Host)\
            .filter(Host.name == name)\
            .first()
        return host


    def create_host(self, name, description=""):
        """Create host."""
        host = Host(name=name, description=description)

        self.db_session.add(host)

        return host


    def get_all_hosts(self):
        """Return all hosts."""
        hosts = self.db_session.query(Host)
        if hosts is None:
            return []

        return hosts

    def get_host_severity(self, host):
        float_trigger_klass = TRIGGER_CLASS.get('float')
        float_alert_klass = ALERT_CLASS.get('float')

        severity = self.db_session.query(TriggerSeverity)\
            .filter(TriggerSeverity.id.in_(\
                self.db_session.query(float_trigger_klass.severity_id)\
                    .filter(float_trigger_klass.item_id.in_(\
                        self.db_session.query(Item.id)\
                            .filter(Item.host_id == host.id)
                    ))\
                    .filter(float_trigger_klass.id.in_(\
                        self.db_session.query(float_alert_klass.trigger_id)\
                            .filter(float_alert_klass.end_time.is_(None))
                    ))
            ))\
            .order_by(TriggerSeverity.level.desc())\
            .first()

        return severity

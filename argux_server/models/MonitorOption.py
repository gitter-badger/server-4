"""Monitor-Option."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    Text,
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

from .Monitor import Monitor


# pylint: disable=too-few-public-methods
class MonitorOption(BASE):

    """MonitorOption Class.

    Base object for referencing MonitorOptions.
    """

    __tablename__ = 'monitor_option'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    monitor_id = Column(Integer, ForeignKey('monitor.id'), nullable=False)
    monitor = relationship(Monitor, backref='options')

Index('u_monitor_option_key_monitor_id_index', MonitorOption.key, MonitorOption.monitor_id, unique=True)


"""MonitorType Model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from . import BASE


# pylint: disable=too-few-public-methods
class MonitorType(BASE):

    """Host Class.

    Base object for referencing Monitors.
    """

    __tablename__ = 'monitor_type'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")

Index('u_monitor_type_id_index', MonitorType.id, unique=True)
Index('u_monitor_type_index', MonitorType.name, unique=True)

"""HostGroup Model."""

from sqlalchemy import (
    Column,
    Index,
    Boolean,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

from .Host import Host


# pylint: disable=too-few-public-methods
class HostGroup(BASE):

    """HostGroup Class.

    Base object for referencing HostGroup.
    """

    __tablename__ = 'host_group'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")

Index('u_host_group_index', HostGroup.name, unique=True, mysql_length=255)

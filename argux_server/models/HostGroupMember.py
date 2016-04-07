"""HostGroupMember Model."""

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
from .HostGroup import HostGroup


# pylint: disable=too-few-public-methods
class HostGroupMember(BASE):

    """HostGroupMember Class.

    Base object for referencing members of a HostGroup.
    """

    __tablename__ = 'host_group_member'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    host_id = Column(
        Integer,
        ForeignKey('host.id'),
        nullable=False)
    host = relationship(Host)
    host_group_id = Column(
        Integer,
        ForeignKey('host_group.id'),
        nullable=False)
    host_group = relationship(HostGroup, backref='members')

Index('i_host_group_member_index', HostGroupMember.host_group_id)

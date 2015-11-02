from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from . import Base

#
# Host
#
class HostDetail(Base):
    __tablename__ = 'host_detail'
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('host.id'), nullable=False)
    name = Column(Text)
    key = Column(Text, nullable=True)
    value = Column(Text, nullable=True)

Index('u_host_detail_index', HostDetail.id, unique=False, mysql_length=255)
Index('u_host_detail_host_id_index', HostDetail.host_id, unique=False, mysql_length=255)

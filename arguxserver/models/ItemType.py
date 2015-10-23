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
# ItemType
#
class ItemType(Base):
    __tablename__ = 'itemtype'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

Index('u_itemtype_name', ItemType.name, unique=True, mysql_length=255)

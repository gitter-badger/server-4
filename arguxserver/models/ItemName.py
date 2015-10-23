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
# ItemName
#
class ItemName(Base):
    __tablename__ = 'itemname'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

Index('u_itemname_name', ItemName.name, unique=True, mysql_length=255)

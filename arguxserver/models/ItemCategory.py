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

from zope.sqlalchemy import ZopeTransactionExtension

from . import Base


#
# ItemCategory
#
class ItemCategory(Base):
    __tablename__ = 'item_category'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

Index('u_itemcategory_name', ItemCategory.name, unique=True, mysql_length=255)

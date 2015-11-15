from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from .ItemName import ItemName
from .ItemType import ItemType
from .ItemCategory import ItemCategory

from . import Base

#
# Item
#
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    key = Column(Text, nullable=False)
    host_id = Column(Integer, ForeignKey('host.id'), nullable=False)
    name_id = Column(Integer, ForeignKey('itemname.id'), nullable=True, default=None)
    name = relationship(ItemName, backref = 'item_name');
    category_id = Column(Integer, ForeignKey('item_category.id'), nullable=True, default=None)
    category = relationship(ItemCategory, backref = 'item_category')
    itemtype_id = Column(Integer, ForeignKey('itemtype.id'), nullable=False)
    itemtype = relationship(ItemType, backref = 'items');
    bookmark = Column(Boolean, default=False, nullable=False)
    bookmark_label = Column(Text, nullable=True)
 
Index('u_item_host_id_index', Item.key, Item.host_id, unique=True, mysql_length=255)

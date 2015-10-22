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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

#
# Host
#
class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

Index('u_host_index', Host.name, unique=True, mysql_length=255)

#
# ItemCategory
#
class ItemCategory(Base):
    __tablename__ = 'item_category'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)

#
# ItemName
#
class ItemName(Base):
    __tablename__ = 'itemname'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

Index('u_itemname_name', ItemName.name, unique=True, mysql_length=255)

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

Index('u_item_host_id_index', Item.key, Item.host_id, unique=True, mysql_length=255)

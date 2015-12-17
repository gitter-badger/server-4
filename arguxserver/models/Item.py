"""Item Module, containing Item model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from .ItemType import ItemType
from .ItemCategory import ItemCategory

from . import BASE


# pylint: disable=too-few-public-methods
class ItemName(BASE):

    """
    ItemName class.

    Model for names for Items.
    """

    __tablename__ = 'itemname'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

Index('u_itemname_name', ItemName.name, unique=True, mysql_length=255)


# pylint: disable=too-few-public-methods
class Item(BASE):

    """
    Item class.

    Model for storing measurement Items.
    """

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    key = Column(Text, nullable=False)
    host_id = Column(Integer, ForeignKey('host.id'), nullable=False)
    name_id = Column(Integer, ForeignKey('itemname.id'), nullable=True, default=None)
    name = relationship(ItemName, backref='item_name')
    category_id = Column(Integer, ForeignKey('item_category.id'), nullable=True, default=None)
    category = relationship(ItemCategory, backref='item_category')
    itemtype_id = Column(Integer, ForeignKey('itemtype.id'), nullable=False)
    itemtype = relationship(ItemType, backref='items')
    bookmark = Column(Boolean, default=False, nullable=False)
    bookmark_label = Column(Text, nullable=True)

Index('u_item_host_id_index', Item.key, Item.host_id, unique=True, mysql_length=255)

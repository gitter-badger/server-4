from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey
    )

from sqlalchemy.orm import (
    relationship
    )

from sqlalchemy.ext.declarative import declared_attr

from .. import Base, DBSession

from ..Item import Item

class AbstractValue():
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    @declared_attr
    def item_id(cls):
        return Column(Integer, ForeignKey('item.id'), nullable=False)

class AbstractSimpleTrigger():
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    rule = Column(Text, nullable=False)

    @declared_attr
    def item_id(cls):
        return Column(Integer, ForeignKey('item.id'), nullable=False)

    @declared_attr
    def item(cls):
        return relationship(Item);

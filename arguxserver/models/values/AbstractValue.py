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

import re

from .. import Base, DBSession

from ..Item import Item

trigger_expr = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?([0-9]*[\.,][0-9]+|[0-9+]))")


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

    @staticmethod
    def validate_rule(rule):
        i = trigger_expr.match(rule)
        if (i == None):
            return False

        ret = [ i.group(1), i.group(2), i.group(3), i.group(4) ]

        if trigger_handlers.get(i.group(1), None) == None:
            return False

        return ret

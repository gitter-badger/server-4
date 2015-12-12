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
from ..TriggerSeverity import TriggerSeverity

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

    trigger_handlers = {}

    @declared_attr
    def severity_id(cls):
        return Column(Integer, ForeignKey('trigger_severity.id'), nullable=False)

    @declared_attr
    def severity(cls):
        return relationship("TriggerSeverity");

    @declared_attr
    def item_id(cls):
        return Column(Integer, ForeignKey('item.id'), nullable=False)

    @declared_attr
    def item(cls):
        return relationship("Item");

    @staticmethod
    def validate_rule(rule):
        i = trigger_expr.match(rule)
        if (i == None):
            return False

        ret = [ i.group(1), i.group(2), i.group(3), i.group(4) ]

        return ret

class AbstractSimpleAlert():
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

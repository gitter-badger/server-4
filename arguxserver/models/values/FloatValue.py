from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from .. import Base, DBSession
from ..Item import Item

import re


trigger_expr = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?([0-9]*[\.,][0-9]+|[0-9+]))")

class FloatValue(Base):
    __tablename__ = 'history_float'
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)

def __handle_last(trigger, selector, operator, value):
    item = trigger.item
    val = DBSession.query(FloatValue) \
            .filter(FloatValue.item_id == item.id) \
            .order_by(FloatValue.timestamp.desc()).first()

    print(operator)

    if operator == '>':
        if val.value > float(value):
            return True
        else:
            return False
    if operator == '<':
        if val.value < float(value):
            return True
        else:
            return False
    if operator == '>=':
        print(str(val.value) +">="+str(value))
        if val.value >= float(value):
            return True
        else:
            return False
    if operator == '<=':
        if val.value >= float(value):
            return True
        else:
            return False

trigger_handlers = {
    "last": __handle_last
}


class FloatSimpleTrigger(Base):
    __tablename__ = 'simple_trigger_float'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    rule = Column(Text, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship(Item);

    @staticmethod
    def validate_rule(rule):
        i = trigger_expr.match(rule)
        if (i == None):
            return False

        ret = [ i.group(1), i.group(2), i.group(3), i.group(4) ]

        if trigger_handlers.get(i.group(1), None) == None:
            return False

        return ret

    def evaluate_rule(self):
        i = trigger_expr.match(self.rule)
        if (i == None):
            return False

        handler = trigger_handlers.get(i.group(1), None)

        if handler:
            return handler(self, i.group(2), i.group(3), i.group(4))
        else:
            return False

class FloatSimpleAlert(Base):
    __tablename__ = 'simple_alert_float'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('simple_trigger_float.id'), nullable=False)
    start_value = Column(Integer, ForeignKey('history_float.id'), nullable=False)
    end_value = Column(Integer, ForeignKey('history_float.id'), nullable=True)

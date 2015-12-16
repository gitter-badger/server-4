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

from .. import BASE
from ..Item import Item

from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger,
    AbstractSimpleAlert
)

from datetime import datetime

import re

trigger_expr = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?([0-9]*[\.,][0-9]+|[0-9+]))")


# pylint: disable=too-few-public-methods
class FloatValue(AbstractValue, BASE):
    __tablename__ = 'history_float'
    value = Column(Float, nullable=True)

Index('floatvalue_ts_index', FloatValue.timestamp, mysql_length=255)


# pylint: disable=too-few-public-methods
class FloatSimpleTrigger(AbstractSimpleTrigger, BASE):

    """FloatSimpleTrigger class.


    Subclass of AbstractSimpleTrigger and BASE.
    """

    __tablename__ = 'simple_trigger_float'

    def __handle_last(trigger, session, selector, operator, value):
        item = trigger.item
        val = session.query(FloatValue) \
                .filter(FloatValue.item_id == item.id) \
                .order_by(FloatValue.timestamp.desc()).first()
        if operator == '>':
            print(val.timestamp.strftime("%Y-%m-%dT%H:%M:%S")+" "+str(val.value) +">"+str(value))
            if val.value > float(value):
                return (True, val.timestamp)
            else:
                return (False, val.timestamp)
        if operator == '<':
            if val.value < float(value):
                return (True, val.timestamp)
            else:
                return (False, val.timestamp)
        if operator == '>=':
            if val.value >= float(value):
                return (True, val.timestamp)
            else:
                return (False, val.timestamp)
        if operator == '<=':
            if val.value >= float(value):
                return (True, val.timestamp)
            else:
                return (False, val.timestamp)

    trigger_handlers = {
        "last": __handle_last
    }


# pylint: disable=too-few-public-methods
class FloatSimpleAlert(AbstractSimpleAlert, BASE):

    """FloatSimpleAlert class.


    Subclass of AbstractSimpleAlert and BASE.
    """

    __tablename__ = 'simple_alert_float'
    trigger_id = Column(Integer, ForeignKey('simple_trigger_float.id'), nullable=False)
    trigger = relationship(FloatSimpleTrigger)

Index('floatsimple_alert_start_ts', FloatSimpleAlert.start_time, mysql_length=255)
Index('floatsimple_alert_end_ts', FloatSimpleAlert.end_time, mysql_length=255)


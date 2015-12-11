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

from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger
)

from datetime import datetime

import re

trigger_expr = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?([0-9]*[\.,][0-9]+|[0-9+]))")


class FloatValue(AbstractValue, Base):
    __tablename__ = 'history_float'
    value = Column(Float, nullable=True)

Index('floatvalue_ts_index', FloatValue.timestamp, mysql_length=255)

class FloatSimpleAlert(Base):
    __tablename__ = 'simple_alert_float'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('simple_trigger_float.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

Index('floatsimple_alert_start_ts', FloatSimpleAlert.start_time, mysql_length=255)
Index('floatsimple_alert_end_ts', FloatSimpleAlert.end_time, mysql_length=255)

def __handle_last(trigger, selector, operator, value):
    item = trigger.item
    val = DBSession.query(FloatValue) \
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


class FloatSimpleTrigger(AbstractSimpleTrigger, Base):
    __tablename__ = 'simple_trigger_float'


    def evaluate_rule(self):
        Session = sessionmaker()
        session = Session()
        i = trigger_expr.match(self.rule)
        if (i == None):
            return False

        handler = trigger_handlers.get(i.group(1), None)

        if handler:
            alert = session.query(FloatSimpleAlert) \
                 .filter(FloatSimpleAlert.trigger_id == self.id) \
                 .filter(FloatSimpleAlert.end_time == None).first()

            (is_active, time) = handler(self, i.group(2), i.group(3), i.group(4))

            if is_active:
                if not alert:
                    alert = FloatSimpleAlert(trigger_id = self.id, start_time = time, end_time=None)
                    session.add(alert)
                    session.commit()
            else:
                if alert:
                    alert.end_time = time
                    session.commit()
            session.close()
        else:
            return False

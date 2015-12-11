from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text, DateTime,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from .. import Base, DBSession

from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger
)


class IntValue(AbstractValue, Base):
    __tablename__ = 'history_int'
    value = Column(Integer, nullable=True)

Index('intvalue_ts_index', IntValue.timestamp, mysql_length=255)

def __handle_last(trigger, selector, operator, value):
    item = trigger.item
    val = DBSession.query(IntValue) \
            .filter(IntValue.item_id == item.id) \
            .order_by(IntValue.timestamp.desc()).first()

    return False

trigger_handlers = {
    "last": __handle_last
}

class IntSimpleTrigger(AbstractSimpleTrigger, Base):
    __tablename__ = 'simple_trigger_int'

    def evaluate_rule(self):
        i = trigger_expr.match(self.rule)
        if (i == None):
            return False

        handler = trigger_handlers.get(i.group(1), None)

        if handler:
            handler(self, i.group(2), i.group(3), i.group(4))
            return True
        else:
            return False

class IntSimpleAlert(Base):
    __tablename__ = 'simple_alert_int'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('simple_trigger_int.id'), nullable=False)
    start_value = Column(Integer, ForeignKey('history_int.id'), nullable=False)
    end_value = Column(Integer, ForeignKey('history_int.id'), nullable=True)

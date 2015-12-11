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

from .. import Base
from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger
)


class TextValue(AbstractValue, Base):
    __tablename__ = 'history_text'
    value = Column(Text, nullable=True)

Index('textvalue_ts_index', TextValue.timestamp, mysql_length=255)

def __handle_last(trigger, selector, operator, value):
    item = trigger.item
    val = DBSession.query(TextValue) \
            .filter(TextValue.item_id == item.id) \
            .order_by(TextValue.timestamp.desc()).first()

    return False

trigger_handlers = {
    "last": __handle_last
}


class TextSimpleTrigger(AbstractSimpleTrigger, Base):
    __tablename__ = 'simple_trigger_text'

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

class TextSimpleAlert(Base):
    __tablename__ = 'simple_alert_text'
    id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey('simple_trigger_text.id'), nullable=False)
    start_value = Column(Integer, ForeignKey('history_text.id'), nullable=False)
    end_value = Column(Integer, ForeignKey('history_text.id'), nullable=True)

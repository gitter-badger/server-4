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

class IntValue(Base):
    __tablename__ = 'history_int'
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)

def __handle_last(trigger, selector, operator, value):
    item = trigger.item
    val = DBSession.query(IntValue) \
            .filter(IntValue.item_id == item.id) \
            .order_by(IntValue.timestamp.desc()).first()

    return False

trigger_handlers = {
    "last": __handle_last
}

class IntSimpleTrigger(Base):
    __tablename__ = 'simple_trigger_int'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    rule = Column(Text, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)

    @staticmethod
    def validate_rule(rule):
        return False

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

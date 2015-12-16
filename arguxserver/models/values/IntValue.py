from sqlalchemy import (
    Column,
    Index,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    scoped_session,
    relationship
)

from arguxserver.util import TRIGGER_EXPR

from .. import BASE

from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger,
    AbstractSimpleAlert
)


# pylint: disable=too-few-public-methods
class IntValue(AbstractValue, BASE):

    """IntValue class.

    Subclass of AbstractValue and BASE.
    """

    __tablename__ = 'history_int'
    value = Column(Integer, nullable=True)

Index('intvalue_ts_index', IntValue.timestamp, mysql_length=255)


# pylint: disable=too-few-public-methods
class IntSimpleTrigger(AbstractSimpleTrigger, BASE):

    """IntSimpleTrigger class.


    Subclass of AbstractSimpleTrigger and BASE.
    """

    __tablename__ = 'simple_trigger_int'

    def evaluate_rule(self):
        i = TRIGGER_EXPR.match(self.rule)
        if (i == None):
            return False

        handler = trigger_handlers.get(i.group(1), None)

        if handler:
            handler(self, i.group(2), i.group(3), i.group(4))
            return True
        else:
            return False

    def __handle_last(trigger, selector, operator, value):
        item = trigger.item

        return False

    trigger_handlers = {
        "last": __handle_last
    }


# pylint: disable=too-few-public-methods
class IntSimpleAlert(AbstractSimpleAlert, BASE):

    """IntSimpleAlert class.


    Subclass of AbstractSimpleAlert and BASE.
    """

    __tablename__ = 'simple_alert_int'
    trigger_id = Column(Integer,
                        ForeignKey('simple_trigger_int.id'),
                        nullable=False)
    trigger = relationship(IntSimpleTrigger)

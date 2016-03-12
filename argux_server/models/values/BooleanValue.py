"""Concrete classes for Triggers and Values of Boolean items."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from .. import BASE
from .AbstractValue import (
    AbstractValue,
    AbstractSimpleTrigger,
    AbstractSimpleAlert
)


# pylint: disable=too-few-public-methods
class BooleanValue(AbstractValue, BASE):

    """BooleanValue class.

    Subclass of AbstractValue and BASE.
    """

    __tablename__ = 'history_boolean'
    value = Column(Boolean, nullable=False)

Index('booleanvalue_ts_index', BooleanValue.timestamp, mysql_length=255)


# pylint: disable=too-few-public-methods
class BooleanSimpleTrigger(AbstractSimpleTrigger, BASE):

    """BooleanSimpleTrigger class.

    Subclass of AbstractSimpleTrigger and BASE.
    """

    __tablename__ = 'simple_trigger_boolean'

    # pylint: disable=unused-argument
    def __handle_last(self, selector, operator, value):
        item = self.item
        val = session.query(BooleanValue)\
            .filter(BooleanValue.item_id == item.id)\
            .order_by(BooleanValue.timestamp.desc()).first()

        if ((operator == '==' and val.value == value) or
                (operator == '!=' and val.value != value)):
            return (True, val.timestamp)
        else:
            return (False, val.timestamp)

    trigger_handlers = {
        "last": __handle_last
    }


# pylint: disable=too-few-public-methods
class BooleanSimpleAlert(AbstractSimpleAlert, BASE):

    """BooleanSimpleAlert class.

    Subclass of AbstractSimpleAlert and BASE.
    """

    __tablename__ = 'simple_alert_boolean'
    trigger_id = Column(Integer, ForeignKey('simple_trigger_boolean.id'), nullable=False)
    trigger = relationship(BooleanSimpleTrigger)

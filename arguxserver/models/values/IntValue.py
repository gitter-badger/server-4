"""Concrete classes for Triggers and Values of Integer items."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
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

    # pylint: disable=unused-argument
    def __handle_last(self, selector, operator, value):
        item = self.item

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

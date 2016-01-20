"""Concrete classes for Triggers and Values of Text items."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
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
class TextValue(AbstractValue, BASE):

    """TextValue class.

    Subclass of AbstractValue and BASE.
    """

    __tablename__ = 'history_text'
    value = Column(Text, nullable=True)

Index('textvalue_ts_index', TextValue.timestamp, mysql_length=255)


# pylint: disable=too-few-public-methods
class TextSimpleTrigger(AbstractSimpleTrigger, BASE):

    """TextSimpleTrigger class.

    Subclass of AbstractSimpleTrigger and BASE.
    """

    __tablename__ = 'simple_trigger_text'

    # pylint: disable=unused-argument
    def __handle_last(self, selector, operator, value):
        item = self.item

        return False

    trigger_handlers = {
        "last": __handle_last
    }


# pylint: disable=too-few-public-methods
class TextSimpleAlert(AbstractSimpleAlert, BASE):

    """TextSimpleAlert class.

    Subclass of AbstractSimpleAlert and BASE.
    """

    __tablename__ = 'simple_alert_text'
    trigger_id = Column(Integer, ForeignKey('simple_trigger_text.id'), nullable=False)
    trigger = relationship(TextSimpleTrigger)

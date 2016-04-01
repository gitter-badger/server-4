"""Concrete classes for Triggers and Values of Decimaling items."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Numeric,
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
class DecimalValue(AbstractValue, BASE):

    """DecimalValue class.

    Subclass of AbstractValue and BASE.
    """

    __tablename__ = 'history_decimal'
    value = Column(Numeric, nullable=True)

Index('decimalvalue_ts_index', DecimalValue.timestamp, mysql_length=255)


# pylint: disable=too-few-public-methods
class DecimalSimpleTrigger(AbstractSimpleTrigger, BASE):

    """DecimalSimpleTrigger class.

    Subclass of AbstractSimpleTrigger and BASE.
    """

    __tablename__ = 'simple_trigger_decimal'


    @staticmethod
    def validate_rule(rule):
        """Validate DecimalSimpleTriger rules."""
        ret = AbstractSimpleTrigger.validate_rule(rule)
        if ret is None:
            return None

        operators = ['!=', '==', '>', '<', '>=', '<=']
        if ret[2] not in operators:
            return None

        return ret

    # pylint: disable=unused-argument
    def __handle_last(self, session, selector, operator, value):

        item = self.item
        val = session.query(DecimalValue)\
            .filter(DecimalValue.item_id == item.id)\
            .order_by(DecimalValue.timestamp.desc()).first()

        # Should be custom error
        if val is None:
            raise ValueError("No Values")

        if ((operator == '>' and val.value > decimal(value)) or
                (operator == '<' and val.value < decimal(value)) or
                (operator == '>=' and val.value >= decimal(value)) or
                (operator == '<=' and val.value <= decimal(value)) or
                (operator == '==' and val.value == decimal(value)) or
                (operator == '!=' and val.value != decimal(value))):
            return (True, val.timestamp)
        else:
            return (False, val.timestamp)

    trigger_handlers = {
        "last": __handle_last
    }


# pylint: disable=too-few-public-methods
class DecimalSimpleAlert(AbstractSimpleAlert, BASE):

    """DecimalSimpleAlert class.

    Subclass of AbstractSimpleAlert and BASE.
    """

    __tablename__ = 'simple_alert_decimal'
    trigger_id = Column(
        Integer,
        ForeignKey('simple_trigger_decimal.id'),
        nullable=False)
    trigger = relationship(DecimalSimpleTrigger)

Index('decimalsimple_alert_start_ts', DecimalSimpleAlert.start_time, mysql_length=255)
Index('decimalsimple_alert_end_ts', DecimalSimpleAlert.end_time, mysql_length=255)


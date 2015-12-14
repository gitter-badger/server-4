"""Abstract classes for Triggers and Values."""

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from sqlalchemy.ext.declarative import declared_attr

from arguxserver.util import TRIGGER_EXPR


#pylint: disable=too-few-public-methods
class AbstractValue(object):

    """
    AbstractValue class.

    All value types must be a subclass of the AbstractValue class.
    """

    id = Column(Integer, primary_key=True) #pylint: disable=invalid-name
    timestamp = Column(DateTime, nullable=False)

    @declared_attr
    def item_id(self):
        return Column(Integer, ForeignKey('item.id'), nullable=False)


#pylint: disable=too-few-public-methods
class AbstractSimpleTrigger(object):

    """
    AbstractSimpleTrigger class.

    All simple-trigger types must be a subclass of
    the AbstractSimpleTrigger class.

    """

    id = Column(Integer, primary_key=True) #pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    rule = Column(Text, nullable=False)

    trigger_handlers = {}

    @declared_attr
    def severity_id(self):
        return Column(Integer, ForeignKey('trigger_severity.id'), nullable=False)

    @declared_attr
    def severity(self):
        return relationship("TriggerSeverity");

    @declared_attr
    def item_id(self):
        return Column(Integer, ForeignKey('item.id'), nullable=False)

    @declared_attr
    def item(self):
        return relationship("Item")

    @staticmethod
    def validate_rule(rule):

        i = TRIGGER_EXPR.match(rule)

        if i == None:
            return False

        ret = [i.group(2), i.group(2), i.group(3), i.group(4)]

        return ret


#pylint: disable=too-few-public-methods
class AbstractSimpleAlert(object):

    """
    AbstractSimpleAlert class.

    All simple-alert types must be a subclass of
    the AbstractSimpleAlert class.
    """

    id = Column(Integer, primary_key=True) #pylint: disable=invalid-name
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

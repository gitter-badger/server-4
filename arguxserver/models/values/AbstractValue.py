from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey
    )

from sqlalchemy.orm import (
    sessionmaker,
    relationship
    )

from sqlalchemy.ext.declarative import declared_attr

import re

from .. import Base, DBSession

from ..Item import Item

trigger_expr = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?([0-9]*[\.,][0-9]+|[0-9+]))")


class AbstractValue():
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    @declared_attr
    def item_id(cls):
        return Column(Integer, ForeignKey('item.id'), nullable=False)

class AbstractSimpleTrigger():
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    rule = Column(Text, nullable=False)

    AlertKlass = None
    trigger_handlers = {}

    @declared_attr
    def item_id(cls):
        return Column(Integer, ForeignKey('item.id'), nullable=False)

    @declared_attr
    def item(cls):
        return relationship(Item);

    @staticmethod
    def validate_rule(rule):
        i = trigger_expr.match(rule)
        if (i == None):
            return False

        ret = [ i.group(1), i.group(2), i.group(3), i.group(4) ]

        if self.trigger_handlers.get(i.group(1), None) == None:
            return False

        return ret

    def evaluate_rule(self):
        if self.AlertKlass == None:
            raise Exception("AlertKlass must be a specified")

        Session = sessionmaker()
        session = Session()
        i = trigger_expr.match(self.rule)
        if (i == None):
            return False

        handler = self.trigger_handlers.get(i.group(1), None)

        if handler:
            alert = session.query(self.AlertKlass) \
                 .filter(self.AlertKlass.trigger_id == self.id) \
                 .filter(self.AlertKlass.end_time == None).first()

            (is_active, time) = handler(self, session, i.group(2), i.group(3), i.group(4))

            if is_active:
                if not alert:
                    alert = AlertKlass(trigger_id = self.id, start_time = time, end_time=None)
                    session.add(alert)
                    session.commit()
            else:
                if alert:
                    alert.end_time = time
                    session.commit()
            session.close()
        else:
            return False

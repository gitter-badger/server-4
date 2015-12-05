from datetime import datetime, timedelta

from arguxserver.models import (
    DBSession,
    Item,
    )

from arguxserver.dao.util import (
    __value_class,
    __trigger_class,
    __alert_class
    )

import re

# NAME(RANGE) EXPR VALUE

trigger_expr = re.compile(r"([a-z]+)\(([0-9]*)\)[ ]*(>|<|>=|<=|==|!=)[ ]*([-]?([0-9]*[\.,][0-9]+|[0-9+]))")

def pushValue(item, timestamp, value):
    value_klass = __value_class.get(item.itemtype.name, None)
    i = value_klass(item_id = item.id, timestamp=timestamp, value=value)
    DBSession.add(i)
    return

def getLastValue(item):
    klass = __value_class.get(item.itemtype.name, lambda: "nothing")
    c = DBSession.query(klass).filter(klass.item_id == item.id).order_by(klass.timestamp.desc()).first()
    return c

def getValues(item, start_time = None, end_time = None, count = -1):
    klass = __value_class.get(item.itemtype.name, "nothing")

    q = DBSession.query(klass) \
            .filter(klass.item_id == item.id)

    if (start_time):
        q = q.filter(
                klass.timestamp > start_time)
    if (end_time):
        q = q.filter(
                klass.timestamp < end_time)

    values = q.order_by(klass.timestamp.asc()).all()

    return values

def getAllTriggers():
    triggers = []
    for name in __trigger_class:
        klass = __trigger_class[name]
        triggers.extend(DBSession.query(klass).all())

    return triggers

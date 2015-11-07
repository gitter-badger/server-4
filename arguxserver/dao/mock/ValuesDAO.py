from datetime import datetime, timedelta

from arguxserver.models import (
    DBSession,
    Item,
    IntValue,
    FloatValue
    )

# Map
__push_value_class = {
    "int" : IntValue,
    "float" : FloatValue
}


def pushValue(item, timestamp, value):
    klass = __push_value_class.get(item.itemtype.name, lambda: "nothing")
    i = klass(item_id = item.id, timestamp=timestamp, value=value)
    DBSession.add(i)
    return

def getLastValue(item):
    klass = __push_value_class.get(item.itemtype.name, lambda: "nothing")
    c = DBSession.query(klass).filter(klass.item_id == item.id).order_by(klass.timestamp.desc()).first()
    return c

def getValues(item):
    klass = __push_value_class.get(item.itemtype.name, lambda: "nothing")

    # Get last value
    c = DBSession.query(klass) \
            .filter(klass.item_id == item.id) \
            .order_by(klass.timestamp.desc()) \
            .first()

    if (c == None):
        return []

    # Get all values of the last 15 minutes before the last.
    a = DBSession.query(klass) \
            .filter(klass.item_id == item.id) \
            .filter(klass.timestamp > c.timestamp - timedelta(minutes=60)) \
            .order_by(klass.timestamp.asc()) \
            .all()
    return a


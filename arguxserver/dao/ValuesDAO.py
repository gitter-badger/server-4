from datetime import datetime, timedelta

from arguxserver.models import (
    DBSession,
    Item,
    IntValue,
    FloatValue,
    TextValue
    )

# Map
__push_value_class = {
    "int" : IntValue,
    "float" : FloatValue,
    "text" : TextValue,
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

def getValues(item, start_time = None, end_time = None, count = -1):
    klass = __push_value_class.get(item.itemtype.name, "nothing")

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

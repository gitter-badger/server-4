
from arguxserver.models import (
    DBSession,
    Item,
    IntValue,
    FloatValue
    )

# Map
__push_value_class = {
    "int" : FloatValue,
    "float" : IntValue
}


def pushValue(item, timestamp, value):
    klass = __push_value_class.get(item.itemtype.name, lambda: "nothing")
    i = klass(item_id = item.id, timestamp=timestamp, value=value)
    DBSession.add(i)
    return

def getValues(item):
    klass = __push_value_class.get(item.itemtype.name, lambda: "nothing")
    c = DBSession.query(klass).filter(klass.item_id == item.id).first()
    return c

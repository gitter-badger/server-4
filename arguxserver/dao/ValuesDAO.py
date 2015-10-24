
from arguxserver.models import (
    DBSession,
    Item,
    IntValue,
    FloatValue
    )

def pushIntValue(item, timestamp, value):
    v = IntValue(item_id = item.id, timestamp=timestamp, value=value)
    DBSession.add(v)
    return

def pushFloatValue(item, ts, value):
    v = FloatValue(item_id = item.id, timestamp=ts, value=value)
    DBSession.add(v)
    return


def pushValue(item, timestamp, value):
    __argux_types = {
        "int" : pushIntValue,
        "float" : pushFloatValue
    }

    func = __argux_types.get(item.itemtype.name, lambda: "nothing")
    return func(item, timestamp, value)


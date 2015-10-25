
from arguxserver.models import (
    DBSession,
    Item,
    IntValue,
    FloatValue
    )

def __pushIntValue(item, timestamp, value):
    v = IntValue(item_id = item.id, timestamp=timestamp, value=value)
    DBSession.add(v)
    return

def __pushFloatValue(item, ts, value):
    v = FloatValue(item_id = item.id, timestamp=ts, value=value)
    DBSession.add(v)
    return

# Map
__push_value_functions = {
    "int" : __pushIntValue,
    "float" : __pushFloatValue
}


def pushValue(item, timestamp, value):
    func = __push_value_functions.get(item.itemtype.name, lambda: "nothing")
    return func(item, timestamp, value)


def __getIntValue(item):
    c = DBSession.query(IntValue).filter(IntValue.item_id == item.id).first()
    return c

def __getFloatValue(item):
    c = DBSession.query(FloatValue).filter(FloatValue.item_id == item.id).first()
    return c


# Map
__get_value_functions = {
    "int" : __getIntValue,
    "float" : __getFloatValue
}


def getValues(item):
    func = __get_value_functions.get(item.itemtype.name, lambda: "nothing")
    return func(item)

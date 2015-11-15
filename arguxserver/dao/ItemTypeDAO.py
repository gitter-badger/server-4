
from arguxserver.models import (
    DBSession,
    ItemType,
    ItemTypeDetail,
    )

def getItemTypeByName(name):
    i = DBSession.query(ItemType).filter(ItemType.name == name).first()
    return i

def addDetail(item_type,name,rule):
    d = ItemTypeDetail(itemtype=item_type, name=name, rule=rule)
    DBSession.add(d)
    return None

def getDetails(item_type):
    return item_type.details

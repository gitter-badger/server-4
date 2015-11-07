
from arguxserver.models import (
    DBSession,
    ItemName
    )

def getItemNameByName(name):
    i = DBSession.query(ItemName).filter(ItemName.name == name).first()
    return i

def createItemName(name, description):
    i = ItemName(name=name,description=description)
    DBSession.add(i)
    return i


from arguxserver.models import (
    DBSession,
    ItemType
    )

def getItemTypeByName(name):
    i = DBSession.query(ItemType).filter(ItemType.name == name).first()
    return i

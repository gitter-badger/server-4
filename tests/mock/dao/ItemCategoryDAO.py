
from arguxserver.models import (
    DBSession,
    ItemCategory
    )

def getItemCategoryByName(name):
    c = DBSession.query(ItemCategory).filter(ItemCategory.name == name).first()
    return c

def createItemCategory(name):
    c = ItemCategory(name=category)
    DBSession.add(c)
    return c

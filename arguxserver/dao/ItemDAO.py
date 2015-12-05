
from arguxserver.models import (
    DBSession,
    Host,
    ItemCategory,
    ItemName,
    Item
    )

from arguxserver.dao.util import (
    __trigger_class
    )

def getItemsFromHost(host):
    i = DBSession.query(Item).filter(Item.host_id == host.id)
    return i

def getItemByHostKey(host, key):
    i = DBSession.query(Item).filter(Item.host_id == host.id).filter(Item.key == key).first()
    return i

def createItem(host, key, name, category, itemtype):
    i = Item(host_id=host.id, key=key, name=name, category=category, itemtype=itemtype)
    DBSession.add(i)
    return i

def createTrigger(item, name, rule, description=""):
    trigger_klass = __trigger_class.get(item.itemtype.name)

    if trigger_klass.validate_rule(rule) == False:
        raise Exception()

    trigger = trigger_klass(name = name, rule=rule, description=description, item_id=item.id)
    DBSession.add(trigger)
    return trigger

def getTriggers(item):
    trigger_klass = __trigger_class.get(item.itemtype.name)
    triggers = DBSession.query(trigger_klass) \
            .filter(trigger_klass.item_id == item.id)

    return triggers

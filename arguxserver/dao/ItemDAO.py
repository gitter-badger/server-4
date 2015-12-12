from datetime import datetime, timedelta

from arguxserver.models import (
    DBSession,
    Host,
    ItemCategory,
    ItemName,
    Item,
    TriggerSeverity
    )

from arguxserver.dao.util import (
    __value_class,
    __trigger_class,
    __alert_class
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

def createTrigger(item, name, rule, description="", severity="info"):
    trigger_klass = __trigger_class.get(item.itemtype.name)

    severity = DBSession.query(TriggerSeverity).filter(TriggerSeverity.key == severity).first()
    if not severity:
        raise Exception()

    if trigger_klass.validate_rule(rule) == False:
        raise Exception()


    trigger = trigger_klass(name = name,
                            rule=rule,
                            description=description,
                            item_id=item.id,
                            severity_id=severity.id)
    DBSession.add(trigger)
    return trigger

def getTriggers(item):
    trigger_klass = __trigger_class.get(item.itemtype.name)
    triggers = DBSession.query(trigger_klass) \
            .filter(trigger_klass.item_id == item.id)

    return triggers

def getAllTriggers():
    triggers = []
    for name in __trigger_class:
        klass = __trigger_class[name]
        triggers.extend(DBSession.query(klass).all())

    return triggers

def pushValue(item, timestamp, value):
    value_klass = __value_class.get(item.itemtype.name, None)
    i = value_klass(item_id = item.id, timestamp=timestamp, value=value)
    DBSession.add(i)
    return

def getLastValue(item):
    klass = __value_class.get(item.itemtype.name, lambda: "nothing")
    c = DBSession.query(klass).filter(klass.item_id == item.id).order_by(klass.timestamp.desc()).first()
    return c

def getValues(item, start_time = None, end_time = None, count = -1):
    klass = __value_class.get(item.itemtype.name, "nothing")

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

def getAlerts(item, active=True, inactive=False):
    alert_klass = __alert_class.get(item.itemtype.name)
    alerts = []
    triggers = getTriggers(item)
    for trigger in triggers:
        a = DBSession.query(alert_klass) \
                .filter(alert_klass.trigger_id == trigger.id) \
                .filter(alert_klass.end_time == None)

        alerts.extend(a)

    return alerts

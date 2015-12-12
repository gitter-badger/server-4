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
    VALUE_CLASS,
    TRIGGER_CLASS,
    ALERT_CLASS
    )

from sqlalchemy.orm import (
    sessionmaker
)

class ItemDAO(object):

    def getItemsFromHost(self, host):
        i = DBSession.query(Item).filter(Item.host_id == host.id)
        return i

    def getItemByHostKey(self, host, key):
        i = DBSession.query(Item).filter(Item.host_id == host.id).filter(Item.key == key).first()
        return i

    def createItem(self, host, key, name, category, itemtype):
        i = Item(host_id=host.id, key=key, name=name, category=category, itemtype=itemtype)
        DBSession.add(i)
        return i

    def createTrigger(self, item, name, rule, description="", severity="info"):
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

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


    def evaluateTrigger(self, trigger):
        item = trigger.item

        alert_klass = ALERT_CLASS.get(item.itemtype.name)

        Session = sessionmaker()
        session = Session()
        i = trigger.validate_rule(trigger.rule)
        if (i == None):
            return False

        handler = trigger.trigger_handlers.get(i[0], None)

        if handler:
            alert = session.query(alert_klass) \
                 .filter(alert_klass.trigger_id == trigger.id) \
                 .filter(alert_klass.end_time == None).first()

            (is_active, time) = handler(trigger, session, i[1], i[2], i[3])

            if is_active:
                if not alert:
                    alert = alert_klass(trigger_id = trigger.id, start_time = time, end_time=None)
                    session.add(alert)
                    session.commit()
            else:
                if alert:
                    alert.end_time = time
                    session.commit()
            session.close()
        else:
            session.close()
            return False

    def getTriggers(self, item):
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)
        triggers = DBSession.query(trigger_klass) \
                .filter(trigger_klass.item_id == item.id)

        return triggers

    def getAllTriggers(self):
        triggers = []
        for name in TRIGGER_CLASS:
            klass = TRIGGER_CLASS[name]
            triggers.extend(DBSession.query(klass).all())

        return triggers

    def pushValue(self, item, timestamp, value):
        value_klass = VALUE_CLASS.get(item.itemtype.name, None)
        i = value_klass(item_id = item.id, timestamp=timestamp, value=value)
        DBSession.add(i)
        return

    def getLastValue(self, item):
        klass = VALUE_CLASS.get(item.itemtype.name, lambda: "nothing")
        c = DBSession.query(klass).filter(klass.item_id == item.id).order_by(klass.timestamp.desc()).first()
        return c

    def getValues(self, item, start_time = None, end_time = None, count = -1):
        klass = VALUE_CLASS.get(item.itemtype.name, "nothing")

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

    def getAlerts(self, item, active=True, inactive=False):
        alert_klass = ALERT_CLASS.get(item.itemtype.name)
        alerts = []
        triggers = self.getTriggers(item)
        for trigger in triggers:
            a = DBSession.query(alert_klass) \
                    .filter(alert_klass.trigger_id == trigger.id) \
                    .filter(alert_klass.end_time == None)

            alerts.extend(a)

        return alerts

    def getItemNameByName(self, name):
        i = DBSession.query(ItemName).filter(ItemName.name == name).first()
        return i

    def createItemName(self, name, description):
        i = ItemName(name=name,description=description)
        DBSession.add(i)
        return i

    def getItemCategoryByName(self, name):
        c = DBSession.query(ItemCategory).filter(ItemCategory.name == name).first()
        return c

    def createItemCategory(self, name):
        c = ItemCategory(name=category)
        DBSession.add(c)
        return c

    def getItemTypeByName(self, name):
        i = DBSession.query(ItemType).filter(ItemType.name == name).first()
        return i

    def addDetail(self, item_type,name,rule):
        d = ItemTypeDetail(itemtype=item_type, name=name, rule=rule)
        DBSession.add(d)
        return None

    def getDetails(self, item_type):
        return item_type.details
